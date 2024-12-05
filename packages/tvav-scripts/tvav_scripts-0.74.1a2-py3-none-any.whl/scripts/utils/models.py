from typing import (
    TYPE_CHECKING,
    Union,
)

from pydantic import BaseSettings

if TYPE_CHECKING:
    from pydantic.typing import (
        AbstractSetIntStr,
        DictStrAny,
        MappingIntStrAny,
    )


class CustomLoadFromEnvModel(BaseSettings):
    """
    CustomLoadFromEnvModel

    ! WARNING: Make sure to have 'pydantic' in your script's requirements.txt

    This class is a customized base class specifically configured for retrieving configuration values
    from environment variables, facilitated by Pydantic.

    It modifies the default .dict() method used in Pydantic to instead return values by_alias while
    omitting any fields with `None` values.

    Beware: You still have the flexibility to pass any parameters to .dict() method consistent with standard
    Pydantic's method usage.

    Unique Advantages:
        1. Permits the manual population of fields using field name.
        2. Supports the automatic loading of environment variables into respective fields during class instantiation.

    Example:
        >>> class BroadcastParameters(CustomLoadFromEnvModel):
        >>>     start_time: datetime = Field(..., env="broadcast_start_time", alias="start_time__gte")
        >>>     end_time: datetime = Field(..., env="broadcast_end_time", alias="start_time__lt")
        >>>
        >>> params = BroadcastParameters()
        >>> params.dict()
        >>> {"start_time__gte": "2023-05-31T22:00:00", "start_time__lt": "2023-06-30T22:00:00"}

        For instance, when instance of Broadcast Parameters is created, the values for BROADCAST_START_TIME and
        BROADCAST_END_TIME from the environment are loaded into their respective fields.
        Utilizing the .dict() method subsequently yields the field values using their respective aliases.

    For an actual usage example check scripts/reportal_v1/v1_reimport_reindex script
    """

    class Config:
        allow_population_by_field_name = True

    def dict(
        self,
        *,
        include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
        by_alias: bool = True,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
    ) -> 'DictStrAny':
        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
