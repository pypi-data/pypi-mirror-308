from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, List, Optional

from . import traverse
from .enums import DimensionType, MemberType
from .models import Annotations


@dataclass(eq=False, frozen=True, order=False)
class TesseractSchema:
    name: str
    locales: List[str]
    default_locale: str
    annotations: Annotations
    cubes: List["TesseractCube"]

    @classmethod
    def from_entity(
        cls,
        entity: traverse.SchemaTraverser,
        roles: Iterable[str] = [],
        locale: Optional[str] = None,
    ):
        """Generates a dataclass-schema object describing this entity."""
        default_locale = entity.schema.default_locale
        locale = default_locale if locale is None else locale
        return cls(
            name=entity.schema.name,
            locales=sorted(entity.get_locale_available()),
            default_locale=default_locale,
            cubes=[
                TesseractCube.from_entity(item, locale)
                for item in entity.cube_map.values()
                if item.visible and item.is_authorized(roles)
            ],
            annotations=dict(entity.schema.annotations),
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractCube:
    name: str
    caption: str
    annotations: Annotations
    dimensions: List["TesseractDimension"]
    measures: List["TesseractMeasure"]

    @classmethod
    @lru_cache(maxsize=256)
    def from_entity(cls, entity: traverse.CubeTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            dimensions=[
                TesseractDimension.from_entity(item, locale)
                for item in entity.dimensions
                if item.visible
            ],
            measures=[
                TesseractMeasure.from_entity(item, locale)
                for item in entity.measures
                if item.visible
            ],
            annotations=dict(entity.annotations),
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractMeasure:
    name: str
    caption: str
    aggregator: str
    annotations: Annotations
    attached: List["TesseractMeasure"]

    @classmethod
    def from_entity(cls, entity: traverse.AnyMeasure, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            aggregator=str(entity.aggregator),
            annotations=dict(entity.annotations),
            attached=[
                cls.from_entity(item, locale)
                for item in entity.submeasures.values()
                if item.visible
            ],
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractDimension:
    name: str
    caption: str
    type: DimensionType
    annotations: Annotations
    hierarchies: List["TesseractHierarchy"]
    default_hierarchy: str

    @classmethod
    def from_entity(cls, entity: traverse.DimensionTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            type=entity.dim_type,
            annotations=dict(entity.annotations),
            hierarchies=[
                TesseractHierarchy.from_entity(item, locale)
                for item in entity.hierarchies
                if item.visible
            ],
            default_hierarchy=entity._entity.default_hierarchy,
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractHierarchy:
    name: str
    caption: str
    annotations: Annotations
    levels: List["TesseractLevel"]

    @classmethod
    def from_entity(cls, entity: traverse.HierarchyTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            annotations=dict(entity.annotations),
            levels=[
                TesseractLevel.from_entity(item, locale)
                for item in entity.levels
                if item.visible
            ],
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractLevel:
    name: str
    caption: str
    depth: int
    annotations: Annotations
    properties: List["TesseractProperty"]

    @classmethod
    def from_entity(cls, entity: traverse.LevelTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            depth=entity.depth,
            annotations=dict(entity.annotations),
            properties=[
                TesseractProperty.from_entity(item, locale)
                for item in entity.properties
                if item.visible
            ],
        )


@dataclass(eq=False, frozen=True, order=False)
class TesseractProperty:
    name: str
    caption: str
    type: MemberType
    annotations: Annotations

    @classmethod
    def from_entity(cls, entity: traverse.PropertyTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            type=entity.key_type,
            annotations=dict(entity.annotations),
        )
