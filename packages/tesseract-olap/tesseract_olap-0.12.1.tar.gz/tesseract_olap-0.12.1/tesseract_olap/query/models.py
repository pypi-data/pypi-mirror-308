"""Query-related internal structs module.

This module contains data-storing structs, used mainly on the query and backend
modules.
"""

import dataclasses as dcls
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
)

from pydantic import BaseModel, model_validator
from typing_extensions import Literal

from tesseract_olap.common import Array, Prim, shorthash
from tesseract_olap.schema import (
    AnyMeasure,
    CalculatedMeasure,
    DimensionTraverser,
    HierarchyTraverser,
    LevelTraverser,
    MemberType,
    PropertyTraverser,
)

from .enums import (
    AnyOrder,
    Comparison,
    JoinType,
    LogicOperator,
    Membership,
    NullityOperator,
    Order,
    RestrictionAge,
    TimeScale,
)

NumericConstraint = Tuple[Union[Comparison, str], float]
ConditionOperator = Union[LogicOperator, Literal["and", "or"]]
MembershipConstraint = Tuple[Membership, Array[str]]

SingleFilterCondition = Tuple[NumericConstraint]
DoubleFilterCondition = Tuple[NumericConstraint, ConditionOperator, NumericConstraint]

FilterCondition = Union[
    NullityOperator,
    # MembershipConstraint,
    SingleFilterCondition,
    DoubleFilterCondition,
]


def parse_filter_condition(value: str) -> FilterCondition:
    if value.lower() in ("isnull", "isnotnull"):
        return NullityOperator.from_str(value)

    if ".and." in value:
        cond1, cond2 = value.split(".and.")
        return (
            parse_numeric_constraint(cond1),
            "and",
            parse_numeric_constraint(cond2),
        )

    if ".or." in value:
        cond1, cond2 = value.split(".or.")
        return (
            parse_numeric_constraint(cond1),
            "or",
            parse_numeric_constraint(cond2),
        )

    return (parse_numeric_constraint(value),)


def parse_numeric_constraint(value: str) -> NumericConstraint:
    comparison, scalar = value.split(".", 1)
    return comparison, float(scalar)


@dcls.dataclass(eq=False, frozen=True, order=False)
class CutIntent:
    """Filtering instructions for a qualitative value.

    Instances of this class are used to define cut parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """

    level: str
    include_members: Set[Prim]
    exclude_members: Set[Prim]

    @classmethod
    def new(cls, level: str, incl: Iterable[Prim], excl: Iterable[Prim]):
        # TODO: enable compatibility for ranged-type include/exclude
        null_values = ("", ",")
        # The include/exclude sets are intended to be used as rules for the
        # composition of the query, so it's not needed to resolve them here.
        include = set(incl).difference(null_values)
        exclude = set(excl).difference(null_values)
        return cls(level=level, include_members=include, exclude_members=exclude)


class FilterIntent(BaseModel):
    """Filtering instructions for a quantitative value.

    Instances of this class are used to define filter parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself.
    """

    field: str
    condition: FilterCondition

    def as_tuple(self):
        return self.field, self.condition

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            field, condition = value.split(".", 1)
            return {"field": field, "condition": parse_filter_condition(condition)}

        return value

    @classmethod
    def new(
        cls,
        field: str,
        condition: Union[
            NumericConstraint, Literal["isnull", "isnotnull"], FilterCondition
        ],
        *,
        and_: Optional[NumericConstraint] = None,
        or_: Optional[NumericConstraint] = None,
    ):
        def _numconst(comp: Tuple[str, float]) -> NumericConstraint:
            return Comparison.from_str(comp[0]), comp[1]

        if condition in ("isnull", "isnotnull"):
            cond = NullityOperator.from_str(condition)
        elif isinstance(condition, NullityOperator):
            cond = condition
        elif len(condition) == 3:
            cond1, oper, cond2 = condition
            cond = (_numconst(cond1), LogicOperator.from_str(oper), _numconst(cond2))
        else:
            constr = condition[0] if len(condition) == 1 else condition
            if and_ is not None:
                cond = (_numconst(constr), LogicOperator.AND, _numconst(and_))
            elif or_ is not None:
                cond = (_numconst(constr), LogicOperator.OR, _numconst(or_))
            else:
                cond = (_numconst(constr),)

        return cls(field=field, condition=cond)


class JoinOnColumns(BaseModel):
    left_on: Union[str, List[str]]
    right_on: Union[str, List[str]]


class JoinIntent(BaseModel):
    """Specifies the intent of the user to perform a Join operation between 2 datasets."""

    on: Union[str, List[str], "JoinOnColumns", None] = None
    how: JoinType = JoinType.LEFT
    suffix: Optional[str] = None
    validate_relation: Literal["m:m", "m:1", "1:m", "1:1"] = "m:m"
    join_nulls: bool = False
    coalesce: Optional[bool] = None


class PaginationIntent(BaseModel):
    """Pagination instructions."""

    limit: int = 0
    offset: int = 0

    def as_tuple(self):
        return self.limit, self.offset

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            limit, offset, *_ = f"{value},0,0".split(",")
            return {"limit": limit, "offset": offset}

        if isinstance(value, (list, tuple)):
            limit, offset, *_ = [*value, 0, 0]
            return {"limit": limit, "offset": offset}

        return value


class SortingIntent(BaseModel):
    """Sorting instructions for internal use."""

    field: str
    order: AnyOrder

    def as_tuple(self):
        return self.field, self.order

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            field, order, *_ = f"{value}..".split(".")
            assert field, "Sorting field must be a valid column name"
            return {"field": field, "order": Order.from_str(order)}

        if isinstance(value, (list, tuple)):
            field, order, *_ = [*value, ""]
            assert field, "Sorting field must be a valid column name"
            return {"field": field, "order": Order.from_str(order)}

        return value


class TimeRestriction(BaseModel):
    """Time-axis filtering instructions for internal use.

    Instances of this class are used to define a time restriction over the
    resulting data. It must always contain both fields."""

    # TODO reformulate fields to use FilterCondition

    level: Union[str, TimeScale]
    age: RestrictionAge
    constraint: Optional[Union[int, str]] = None

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            level, age, *constr = value.split(".", 2)

            assert level, (
                "Time restriction needs to specify a level from a time dimension, "
                "or a valid time scale available as level in this cube."
            )
            # Attempt to match a TimeScale, else use value as Level name
            gen_scale = (item for item in TimeScale if item.value == level)
            level = next(gen_scale, level)

            constraint = constr[0] if len(constr) == 1 else 1

            if age.lower() in ["latest", "last"]:
                age = RestrictionAge.LATEST
            elif age.lower() in ["oldest", "earliest"]:
                age = RestrictionAge.OLDEST
            elif age.lower() in {x.value for x in Comparison}:
                constraint = f"{age}.{constraint}"
                age = RestrictionAge.EXPR
            elif age.lower() in {x.value for x in NullityOperator}:
                constraint = age
                age = RestrictionAge.EXPR
            else:
                raise ValueError(f"Can't parse an age for the data: '{age}'")

            return {"level": level, "age": age, "constraint": constraint}

        return value


class TopkIntent(BaseModel):
    """Limits the results to the K first/last elements in subsets determined by
    one or more levels and their associated value. Adds a column that indicates
    the position of each element in that ranking."""

    levels: Tuple[str, ...]
    measure: str
    order: AnyOrder = Order.DESC
    amount: int = 1

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            amount, levels, measure, order, *_ = f"{value}....".split(".")
            assert levels, (
                "Topk 'levels' field must contain at least a valid level name "
                "from the drilldowns in your request."
            )
            assert measure, (
                "Topk 'measure' field must contain a valid measure name "
                "from the measures in your request."
            )
            return {
                "amount": amount,
                "levels": levels.split(","),
                "measure": measure,
                "order": Order.from_str(order),
            }

        return value


class GrowthIntent(BaseModel):
    """Calculation of growth with respect to a time parameter and a measure"""

    time_level: str
    measure: str
    method: Union[
        Tuple[Literal["period"], int],
        Tuple[Literal["fixed"], str],
    ] = ("period", 1)

    @model_validator(mode="before")
    @classmethod
    def parse(cls, value: Any):
        if isinstance(value, str):
            time_level, measure, *params = value.split(".")
            assert time_level, (
                "Growth calculation requires the name of a level from a "
                "time dimension included in your request."
            )
            assert measure, (
                "Growth calculation must contain a valid measure name "
                "from the measures in your request."
            )
            assert len(params) > 1, (
                "Growth calculation method requires 2 parameters: "
                "'fixed' and the member key to use as anchor value, or "
                "'period' and an integer for how many periods to take as difference."
            )
            if params[0] == "fixed":
                method = ("fixed", params[1])
            else:
                method = ("period", int(params[1]))
            return {"time_level": time_level, "measure": measure, "method": method}

        return value


@dcls.dataclass(eq=True, frozen=True, order=False)
class HierarchyField:
    """Contains the parameters associated to a slicing operation on the data,
    based on a single Hierarchy from a Cube's Dimension.
    """

    dimension: "DimensionTraverser"
    hierarchy: "HierarchyTraverser"
    levels: Tuple["LevelField", ...]

    @property
    def alias(self) -> str:
        """Returns a deterministic unique short ID for the entity."""
        return shorthash(self.dimension.name + self.hierarchy.primary_key)

    @property
    def cut_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_cut)

    @property
    def drilldown_levels(self) -> Iterable["LevelField"]:
        return (item for item in self.levels if item.is_drilldown)

    @property
    def deepest_level(self) -> "LevelField":
        """Returns the deepest LevelField requested in this Hierarchy, for this
        query operation."""
        # TODO: check if is needed to force this to use drilldowns only
        return self.levels[-1]

    @property
    def foreign_key(self) -> str:
        """Returns the column in the fact table of the Cube this Dimension
        belongs to, that matches the primary key of the items in the dim_table.
        """
        return self.dimension.foreign_key  # type: ignore

    @property
    def has_drilldowns(self) -> bool:
        """Verifies if any of the contained LevelFields is being used as a
        drilldown."""
        return any(self.drilldown_levels)

    @property
    def primary_key(self) -> str:
        """Returns the column in the dimension table for the parent Dimension,
        which is used as primary key for the whole set of levels in the chosen
        Hierarchy."""
        return self.hierarchy.primary_key

    @property
    def table(self):
        """Returns the table to use as source for the Dimension data. If not
        set, the data is stored directly in the fact table for the Cube."""
        return self.hierarchy.table


@dcls.dataclass(eq=True, frozen=True, order=False, repr=False)
class LevelField:
    """Contains the parameters associated to the slice operation, specifying the
    columns each resulting group should provide to the output data.
    """

    level: "LevelTraverser"
    caption: Optional["PropertyTraverser"] = None
    is_drilldown: bool = False
    members_exclude: Set[str] = dcls.field(default_factory=set)
    members_include: Set[str] = dcls.field(default_factory=set)
    properties: FrozenSet["PropertyTraverser"] = dcls.field(default_factory=frozenset)
    time_restriction: Optional[TimeRestriction] = None

    def __repr__(self):
        params = (
            f"name={repr(self.level.name)}",
            f"is_drilldown={repr(self.is_drilldown)}",
            f"caption={repr(self.caption)}",
            f"properties={repr(sorted(self.properties, key=lambda x: x.name))}",
            f"cut_exclude={repr(sorted(self.members_exclude))}",
            f"cut_include={repr(sorted(self.members_include))}",
            f"time_restriction={repr(self.time_restriction)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def alias(self) -> str:
        """Returns a deterministic unique short ID for the entity."""
        return shorthash(self.level.name + self.level.key_column)

    @property
    def is_cut(self) -> bool:
        return len(self.members_exclude) + len(self.members_include) > 0

    @property
    def key_column(self) -> str:
        return self.level.key_column

    @property
    def name(self) -> str:
        return self.level.name

    def iter_columns(self, locale: str):
        """Generates triads of (column name, column alias, pair hash) for all fields related to
        a HierarchyField object.

        This comprises Drilldown Labels and IDs, and its requested Properties.
        """
        name = self.level.name
        key_column = self.level.key_column
        name_column = self.level.get_name_column(locale)
        if name_column is None:
            yield key_column, name, shorthash(name + key_column)
        else:
            yield key_column, f"{name} ID", shorthash(name + key_column)
            yield name_column, name, shorthash(name + name_column)
        for propty in self.properties:
            propty_column = propty.get_key_column(locale)
            yield propty_column, propty.name, shorthash(propty.name + propty_column)


@dcls.dataclass(eq=True, frozen=True, order=False, repr=False)
class MeasureField:
    """MeasureField dataclass.

    Contains the parameters needed to filter the data points returned by the
    query operation from the server.
    """

    measure: "AnyMeasure"
    is_measure: bool = False
    constraint: Optional[FilterCondition] = None
    with_ranking: Optional[Literal["asc", "desc"]] = None

    def __repr__(self):
        params = (
            f"name={repr(self.measure.name)}",
            f"is_measure={repr(self.is_measure)}",
            f"constraint={repr(self.constraint)}",
            f"with_ranking={repr(self.with_ranking)}",
        )
        return f"{type(self).__name__}({', '.join(params)})"

    @property
    def alias_name(self):
        """Returns a deterministic short hash of the name of the entity."""
        return shorthash(self.measure.name)

    @property
    def alias_key(self):
        """Returns a deterministic hash of the key column of the entity."""
        return shorthash(
            repr(self.measure.formula)
            if isinstance(self.measure, CalculatedMeasure)
            else self.measure.key_column
        )

    @property
    def name(self) -> str:
        """Quick method to return the measure name."""
        return self.measure.name

    @property
    def aggregator_params(self) -> Dict[str, str]:
        """Quick method to retrieve the measure aggregator params."""
        return self.measure.aggregator.get_params()

    @property
    def aggregator_type(self) -> str:
        """Quick method to retrieve the measure aggregator type."""
        return str(self.measure.aggregator)

    def get_source(self):
        # TODO add locale compatibility
        """Quick method to obtain the source information of the measure."""
        return self.measure.annotations.get("source")

    @property
    def datatype(self):
        return MemberType.FLOAT64
