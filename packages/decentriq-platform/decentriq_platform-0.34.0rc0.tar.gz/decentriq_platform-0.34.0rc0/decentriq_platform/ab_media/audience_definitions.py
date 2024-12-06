from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from .helper import generate_id, current_iso_standard_utc_time
from typing_extensions import Self


class FilterOperator(str, Enum):
    CONTAINS_ANY = "contains_any_of"
    CONTAINS_NONE = "contains_none_of"
    CONTAINS_ALL = "contains_all_of"
    EMPTY = "empty"
    NOT_EMPTY = "not_empty"


class Filter:
    def __init__(
        self, attribute: str, values: List[str], operator: FilterOperator
    ) -> None:
        self.attribute = attribute
        self.values = values
        self.operator = operator

    def as_dict(self) -> Dict[str, Any]:
        return {
            "operator": self.operator.value,
            "attribute": self.attribute,
            "values": self.values,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Self:
        return cls(
            attribute=d["attribute"],
            values=d["values"],
            operator=FilterOperator(d["operator"]),
        )


class MatchOperator(str, Enum):
    # All filter criteria must be satisfied.
    MATCH_ALL = "and"
    # Any filter criteria may be satisfied.
    MATCH_ANY = "or"


class AudienceFilters:
    def __init__(
        self,
        filters: List[Filter],
        operator: MatchOperator,
    ) -> None:
        self.filters = filters
        self.operator = operator

    def as_dict(self) -> Dict[str, Any]:
        return {
            "boolean_op": self.operator.value,
            "filters": [f.as_dict() for f in self.filters],
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Self:
        return cls(
            filters=[Filter.from_dict(f) for f in d["filters"]],
            operator=MatchOperator(d["boolean_op"]),
        )


class CombineOperator(str, Enum):
    # Users in both audiences.
    INTERSECT = "intersect"
    # All users.
    UNION = "union"
    # Users in first audience only.
    DIFF = "diff"


class AudienceCombinator:
    def __init__(
        self,
        operator: CombineOperator,
        source_audience_name: str,
        filters: Optional[AudienceFilters] = None,
        source_ref_id: Optional[str] = None,
    ) -> None:
        self.operator = operator
        self.source_ref_name = source_audience_name
        self.source_ref_id = source_ref_id
        self.filters = filters

    def _set_source_ref_id(self, audiences: Dict[str, Any]):
        # The user works in terms of audience names, so we must
        # lookup the source ID from its name.
        if self.source_ref_name not in audiences:
            raise Exception(
                f'Source audience "{self.source_ref_name}" is not in list of audiences'
            )
        self.source_ref_id = audiences[self.source_ref_name]["id"]

    def as_dict(self) -> Dict[str, Any]:
        if not self.source_ref_id:
            raise Exception("Source ref ID has not been set")

        return {
            "operator": self.operator.value,
            "source_ref": self.source_ref_id,
            "filters": self.filters.as_dict() if self.filters else None,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any], audiences: Dict[str, Any]) -> Self:
        return cls(
            operator=CombineOperator(d["operator"]),
            source_audience_name=audience_name_from_id(d["source_ref"], audiences),
            filters=AudienceFilters.from_dict(d["filters"]) if d["filters"] else None,
            source_ref_id=d["source_ref"],
        )


class AudienceStatus(str, Enum):
    READY = "ready"
    PUBLISHED = "published"


class RuleBasedAudienceDefinition:
    def __init__(
        self,
        name: str,
        source_ref_name: str,
        status: AudienceStatus,
        filters: Optional[AudienceFilters] = None,
        combinators: Optional[List[AudienceCombinator]] = None,
        id: Optional[str] = None,
        created_at: Optional[str] = None,
        source_ref_id: Optional[str] = None,
    ) -> None:
        self.name = name
        self.id = id if id else generate_id()
        self.source_ref_name = source_ref_name
        self.source_ref_id = source_ref_id if source_ref_id else None
        self.status = status
        self.filters = filters
        self.combinators = combinators
        self.kind = "rulebased"
        self.created_at = created_at if created_at else current_iso_standard_utc_time()

    def _set_source_ref_id(self, audiences_by_name: Dict[str, Any]):
        # The user works in terms of audience names, so we must
        # lookup the source ID from its name.
        if self.source_ref_name not in audiences_by_name:
            raise Exception(
                f'Source audience "{self.source_ref_name}" is not in list of audiences'
            )
        self.source_ref_id = audiences_by_name[self.source_ref_name]["id"]

        if self.combinators:
            for c in self.combinators:
                c._set_source_ref_id(audiences_by_name)

    def as_dict(self) -> Dict[str, Any]:
        if not self.source_ref_id:
            raise Exception("Source ref ID has not been set")

        return {
            "id": self.id,
            "kind": self.kind,
            "source_ref": self.source_ref_id,
            "filters": self.filters.as_dict() if self.filters else None,
            "combine": (
                [c.as_dict() for c in self.combinators] if self.combinators else None
            ),
            "mutable": {
                "name": self.name,
                "status": self.status.value,
                "created_at": self.created_at,
            },
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any], audiences: Dict[str, Any]) -> Self:
        (name, status, created_at) = get_mutable_variables(d["mutable"])
        return cls(
            name=name,
            source_ref_name=audience_name_from_id(d["source_ref"], audiences),
            status=status,
            filters=AudienceFilters.from_dict(d["filters"]) if d["filters"] else None,
            combinators=(
                [
                    AudienceCombinator.from_dict(c, audiences=audiences)
                    for c in d["combine"]
                ]
                if d["combine"]
                else None
            ),
            id=d["id"],
            created_at=created_at,
            source_ref_id=d["source_ref"],
        )


class LookalikeAudienceDefinition:
    def __init__(
        self,
        name: str,
        reach: int,
        seed_audience_name: str,
        exclude_seed_audience: bool,
        status: AudienceStatus,
        id: Optional[str] = None,
        created_at: Optional[str] = None,
        source_ref_id: Optional[str] = None,
    ) -> None:
        self.name = name
        self.id = id if id else generate_id()
        self.reach = reach
        self.source_ref_name = seed_audience_name
        self.exclude_seed_audience = exclude_seed_audience
        self.status = status
        self.source_ref_id = source_ref_id if source_ref_id else None
        self.kind = "lookalike"
        self.created_at = created_at if created_at else current_iso_standard_utc_time()

    def _set_source_ref_id(self, audiences_by_name: Dict[str, Any]):
        # The user works in terms of audience names, so we must
        # lookup the source ID from its name.
        if self.source_ref_name not in audiences_by_name:
            raise Exception(
                f'Seed audience "{self.source_ref_name}" is not in list of audiences'
            )
        self.source_ref_id = audiences_by_name[self.source_ref_name]["id"]

    def as_dict(self) -> Dict[str, Any]:
        if not self.source_ref_id:
            raise Exception("Source ref ID has not been set")

        return {
            "id": self.id,
            "kind": self.kind,
            "source_ref": self.source_ref_id,
            "reach": self.reach,
            "exclude_seed_audience": self.exclude_seed_audience,
            "mutable": {
                "name": self.name,
                "status": self.status,
                "created_at": self.created_at,
            },
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any], audiences: Dict[str, Any]) -> Self:
        (name, status, created_at) = get_mutable_variables(d["mutable"])
        return cls(
            name=name,
            reach=d["reach"],
            seed_audience_name=audience_name_from_id(d["source_ref"], audiences),
            exclude_seed_audience=d["exclude_seed_audience"],
            status=status,
            id=d["id"],
            created_at=created_at,
            source_ref_id=d["source_ref"],
        )


class AdvertiserAudienceDefinition:
    def __init__(
        self,
        name: str,
        audience_size: int,
        audience_type: str,
        status: AudienceStatus,
        id: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> None:
        self.name = name
        self.audience_size = audience_size
        self.audience_type = audience_type
        self.id = id if id else generate_id()
        self.kind = "advertiser"
        self.status = status
        self.created_at = created_at if created_at else current_iso_standard_utc_time()

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "audience_size": self.audience_size,
            "audience_type": self.audience_type,
            "mutable": {
                "name": self.name,
                "status": self.status,
                "created_at": self.created_at,
            },
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any], audiences: Dict[str, Any]) -> Self:
        (name, status, created_at) = get_mutable_variables(d["mutable"])
        return cls(
            name=name,
            audience_size=d["audience_size"],
            audience_type=d["audience_type"],
            status=status,
            id=d["id"],
            created_at=created_at,
        )


def audience_name_from_id(audience_id: str, audiences: Dict[str, Any]) -> str:
    lookup = {a["id"]: a["mutable"]["name"] for a in audiences}
    if audience_id not in lookup:
        raise Exception(f'Audience with ID "{audience_id}" could not be found')
    return lookup[audience_id]


def get_mutable_variables(mutable: Dict[str, Any]) -> Tuple[str, AudienceStatus, str]:
    name = mutable["name"]
    status = AudienceStatus(mutable["status"])
    created_at = mutable["created_at"] if "created_at" in mutable else None
    return (name, status, created_at)
