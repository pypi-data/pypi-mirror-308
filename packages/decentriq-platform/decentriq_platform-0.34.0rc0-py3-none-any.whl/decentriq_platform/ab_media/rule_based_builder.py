from typing import List
from typing_extensions import Self
from .audience_definitions import (
    AudienceFilters,
    AudienceCombinator,
    RuleBasedAudienceDefinition,
    AudienceStatus,
)


class RuleBasedAudienceBuilder:
    """
    Builder for constructing rule-based audience definitions.
    """

    def __init__(self, name: str, source_audience_name: str) -> None:
        """
        Initialise the rule-based audience builder.
        """
        self.name = name
        self.source_audience_name = source_audience_name
        self.make_available_to_publisher = False
        self.filters = None
        self.combinators = None

    def with_make_available_to_publisher(self) -> Self:
        """
        Make the rule-based audience available to the publisher.
        """
        self.make_available_to_publisher = True
        return self

    def with_filters(self, filters: AudienceFilters) -> Self:
        """
        Set the filters to be applied to the source audience.

        **Parameters**:
        - `filters`: Filters to be applied to the source audience.
        """
        self.filters = filters
        return self

    def with_combinator(self, combinators: List[AudienceCombinator]) -> Self:
        """
        Set the combinators to be applied to the audiences.
        This defines how multiple audiences can be combined.

        **Parameters**:
        - `combinators`: The list of combinators used to combine audiences.
        """
        self.combinators = combinators
        return self

    def build(self) -> RuleBasedAudienceDefinition:
        """
        Build the rule-based audience definition.
        """
        return RuleBasedAudienceDefinition(
            name=self.name,
            source_ref_name=self.source_audience_name,
            status=(
                AudienceStatus.PUBLISHED
                if self.make_available_to_publisher
                else AudienceStatus.READY
            ),
            filters=self.filters,
            combinators=self.combinators,
        )
