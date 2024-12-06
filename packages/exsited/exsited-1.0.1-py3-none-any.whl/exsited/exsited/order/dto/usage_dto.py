from dataclasses import dataclass
from exsited.exsited.common.dto.common_dto import CustomAttributesDTO
from exsited.sdlize.ab_base_dto import ABBaseDTO
@dataclass(kw_only=True)
class UsageDataDTO(ABBaseDTO):
    chargeItemUuid: str = None
    chargingPeriod: str = None
    quantity: str = None
    startTime: str = None
    endTime: str = None
    type: str = None
    customAttributes: list[CustomAttributesDTO] = None


@dataclass(kw_only=True)
class UsageCreateDTO(ABBaseDTO):
    usage: UsageDataDTO = None