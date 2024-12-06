from typing_extensions import Self
from .audience_definitions import LookalikeAudienceDefinition, AudienceStatus


class LookalikeAudienceBuilder:
    """
    Builder for constructing lookalike audience definitions.
    """

    def __init__(self, name: str, reach: int, source_audience_name: str) -> None:
        """
        Initialise the lookalike audience builder.
        """
        if not (0 <= reach <= 30):
            raise Exception(f"Reach value {reach} is not in range 0 to 30")

        self.name = name
        self.reach = reach
        self.source_audience_name = source_audience_name
        self.exclude_seed_audience = False
        self.make_available_to_publisher = False

    def with_exclude_seed_audience(self) -> Self:
        """
        Exclude the seed audience from the lookalike audience.
        """
        self.exclude_seed_audience = True
        return self

    def with_make_available_to_publisher(self) -> Self:
        """
        Make the lookalike audience available to the publisher.
        """
        self.make_available_to_publisher = True
        return self

    def build(self) -> LookalikeAudienceDefinition:
        """
        Build the lookalike audience definition.
        """
        return LookalikeAudienceDefinition(
            name=self.name,
            reach=self.reach,
            seed_audience_name=self.source_audience_name,
            exclude_seed_audience=self.exclude_seed_audience,
            status=(
                AudienceStatus.PUBLISHED
                if self.make_available_to_publisher
                else AudienceStatus.READY
            ),
        )
