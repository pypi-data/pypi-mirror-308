import logging
from typing import List, Optional, Tuple, Union, overload

import clickhouse_driver as chdr
import polars as pl
from clickhouse_driver.dbapi import DatabaseError, InterfaceError
from clickhouse_driver.dbapi.extras import Cursor, DictCursor, NamedTupleCursor
from pypika.queries import Selectable
from typing_extensions import Literal

from tesseract_olap.backend import (
    Backend,
    CacheProvider,
    DummyProvider,
    ParamManager,
    Result,
    Session,
    growth_calculation,
)
from tesseract_olap.common import AnyDict, AnyTuple, hide_dsn_password
from tesseract_olap.exceptions.backend import UpstreamInternalError, UpstreamNotPrepared
from tesseract_olap.query import AnyQuery, DataQuery, MembersQuery, PaginationIntent
from tesseract_olap.schema import InlineTable, SchemaTraverser

from .dialect import ClickhouseDataType
from .sqlbuild import dataquery_sql, membersquery_sql

logger = logging.getLogger("tesseract_olap.backend.clickhouse")


class ClickhouseBackend(Backend):
    """Clickhouse Backend class

    This is the main implementation for Clickhouse of the core :class:`Backend`
    class.

    Must be initialized with a connection string with the parameters for the
    Clickhouse database. Then must be connected before used to execute queries,
    and must be closed after finishing use.
    """

    dsn: str

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn

    def new_session(self, cache: Optional["CacheProvider"] = None, **kwargs):
        if cache is None:
            cache = DummyProvider()
        return ClickhouseSession(self.dsn, cache=cache, **kwargs)

    def ping(self) -> bool:
        """Checks if the current connection is working correctly."""
        with self.new_session() as session:
            with session.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
        return result == (1,)

    def generate_sql(self, query: "AnyQuery", **kwargs) -> str:
        qbuilder, meta = _query_to_builder(query)
        sql = qbuilder.get_sql()
        if meta.params:
            sql += "\nWITH PARAMS " + repr(meta.params)
        for table in meta.tables:
            columns = ", ".join(
                f"{header} {dtype}" for header, dtype in zip(table.headers, table.types)
            )
            sql += f"\nWITH INLINE TABLE {table.name}({columns})"
        return sql

    def validate_schema(self, schema: "SchemaTraverser"):
        """Checks all the tables and columns referenced in the schema exist in
        the backend.
        """
        logger.debug("Validating schema '%s' against backend", schema)

        tables = schema.unwrap_tables()

        query_template = """
SELECT
    '{table_name}' AS "table",
    arrayMap(x -> x.1, columns) AS "columns",
    (SELECT count(*) FROM {table_name}) AS "count"
FROM system.columns
WHERE table = '{table_name}'
""".strip()
        query = " UNION ALL ".join(
            query_template.format(table_name=table_name) for table_name in tables.keys()
        )

        with self.new_session() as session:
            with session.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall() or []

        observed: dict[str, set[str]] = {item[0]: set(item[1]) for item in result}

        assert tables == observed


class ClickhouseSession(Session):
    def __init__(self, dsn: str, *, cache: "CacheProvider"):
        self.cache = cache
        self.dsn = dsn

    def __repr__(self):
        return f"{type(self).__name__}(dsn='{hide_dsn_password(self.dsn)}')"

    def __exit__(self, exc_type, exc_val, exc_tb):
        result = super().__exit__(exc_type, exc_val, exc_tb)
        try:
            args = getattr(exc_val, "args")
        except AttributeError:
            args = tuple()

        if exc_type is InterfaceError:
            raise UpstreamNotPrepared(*args) from exc_val
        if exc_type is DatabaseError:
            raise UpstreamInternalError(*args) from exc_val

        return result

    def connect(self):
        self._cache = self.cache.connect()
        self._connection = chdr.connect(dsn=self.dsn, compression="lz4")

    def close(self):
        self._cache.close()
        self._connection.close()
        delattr(self, "_cache")
        delattr(self, "_connection")

    def fetch(self, query: AnyQuery, **kwargs) -> Result[List[AnyTuple]]:
        qbuilder, meta = _query_to_builder(query)

        with self.cursor() as cursor:
            _tables_into_cursor(cursor, meta.tables)
            cursor.execute(qbuilder.get_sql(), parameters=meta.params)
            data = cursor.fetchall() or []

        limit, offset = query.pagination.as_tuple()

        return Result(
            data=data,
            columns=query.columns,
            cache={"key": query.key, "status": "MISS"},
            page={"limit": limit, "offset": offset, "total": len(data)},
        )

    def fetch_dataframe(self, query: AnyQuery, **kwargs) -> Result[pl.DataFrame]:
        pagi = query.pagination
        if pagi.limit > 0 or pagi.offset > 0:
            query.pagination = PaginationIntent(limit=0, offset=0)

        data = self._cache.retrieve(query)
        if data is None:
            cache_status = "MISS"
            qbuilder, meta = _query_to_builder(query)

            with self.cursor() as cursor:
                _tables_into_cursor(cursor, meta.tables)
                data = pl.read_database(
                    query=qbuilder.get_sql(),
                    connection=cursor,
                    execute_options={"parameters": meta.params},
                )

            self._cache.store(query, data)
        else:
            cache_status = "HIT"

        # TODO: maybe move the data.slice here?

        # Resolve internally if query is DataQuery and has GrowthIntent
        data = growth_calculation(query, data)

        logger.debug(f"Cache: {type(self.cache).__name__} {cache_status} {query.key}")
        result = Result(
            data=data.slice(pagi.offset, pagi.limit or None),
            columns=query.columns,
            cache={"key": query.key, "status": cache_status},
            page={"limit": pagi.limit, "offset": pagi.offset, "total": data.height},
        )

        if pagi.limit > 0 or pagi.offset > 0:
            query.pagination = pagi

        return result

    def fetch_records(self, query: AnyQuery, **kwargs) -> Result[List[AnyDict]]:
        qbuilder, meta = _query_to_builder(query)

        with self.cursor("Dict") as cursor:
            _tables_into_cursor(cursor, meta.tables)
            cursor.execute(qbuilder.get_sql(), parameters=meta.params)
            data: List[AnyDict] = cursor.fetchall()  # type: ignore

        limit, offset = query.pagination.as_tuple()

        return Result(
            data=data,
            columns=query.columns,
            cache={"key": query.key, "status": "MISS"},
            page={"limit": limit, "offset": offset, "total": len(data)},
        )

    @overload
    def cursor(self) -> "TypedCursor": ...
    @overload
    def cursor(self, format_: Literal["Tuple"]) -> "TypedCursor": ...
    @overload
    def cursor(self, format_: Literal["Dict"]) -> "TypedDictCursor": ...
    @overload
    def cursor(self, format_: Literal["NamedTuple"]) -> "NamedTupleCursor": ...

    def cursor(
        self, format_: Literal["Dict", "Tuple", "NamedTuple"] = "Tuple"
    ) -> Union["Cursor", "DictCursor", "NamedTupleCursor"]:
        if format_ == "Dict":
            cls = DictCursor
        elif format_ == "Tuple":
            cls = Cursor
        elif format_ == "NamedTuple":
            cls = NamedTupleCursor
        else:
            raise ValueError(f"Invalid cursor result format: '{format_}'")

        return self._connection.cursor(cls)


def _query_to_builder(query: AnyQuery) -> Tuple[Selectable, ParamManager]:
    if isinstance(query, DataQuery):
        return dataquery_sql(query)

    if isinstance(query, MembersQuery):
        return membersquery_sql(query)


def _tables_into_cursor(cursor: Cursor, tables: List["InlineTable"]):
    for table in tables:
        tblmeta_gen = (ClickhouseDataType[item.name].value for item in table.types)
        structure = zip(table.headers, tblmeta_gen)
        cursor.set_external_table(table.name, list(structure), table.rows)


class TypedCursor(Cursor):
    _columns: List[str]
    _columns_with_types: List[Tuple[str, str]]


class TypedDictCursor(DictCursor):
    """
    A cursor that generates results as :class:`dict`.

    ``fetch*()`` methods will return dicts instead of tuples.
    """

    _columns: List[str]
    _columns_with_types: List[Tuple[str, str]]
