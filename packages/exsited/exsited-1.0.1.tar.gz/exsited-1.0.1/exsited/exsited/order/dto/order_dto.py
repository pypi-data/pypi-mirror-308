from dataclasses import dataclass
from exsited.exsited.common.dto.common_dto import CustomFormsDTO, CurrencyDTO, TimeZoneDTO, TaxDTO, PaginationDTO
from exsited.exsited.order.dto.order_nested_dto import OrderLineDTO, OrderItemPriceSnapshotDTO, OrderPropertiesDTO
from exsited.sdlize.ab_base_dto import ABBaseDTO


@dataclass(kw_only=True)
class OrderDataDTO(ABBaseDTO):
    accountId: str
    status: str = None
    id: str = None
    uuid: str = None
    version: str = None
    preOrder: str = None
    quoteOrder: str = None
    name: str = None
    displayName: str = None
    description: str = None
    manager: str = None
    referralAccount: str = None
    shippingCost: str = None
    origin: str = None
    invoiceNote: str = None
    billingStartDate: str = None
    orderStartDate: str = None
    nextBillingFromDate: str = None
    priceTaxInclusive: str = None
    createdBy: str = None
    createdOn: str = None
    lastUpdatedBy: str = None
    lastUpdatedOn: str = None
    allowContract: str = None

    lines: list[OrderLineDTO] = None
    customForms: CustomFormsDTO = None
    currency: CurrencyDTO = None
    timeZone: TimeZoneDTO = None
    properties: OrderPropertiesDTO = None

    def add_line(self, item_id: str, quantity: str, price: str = None):
        line = OrderLineDTO(itemId=item_id, itemOrderQuantity=quantity)
        if price:
            line.itemPriceSnapshot = OrderItemPriceSnapshotDTO().add_rule(price=price)
        if not self.lines:
            self.lines = []
        self.lines.append(line)
        return self


@dataclass(kw_only=True)
class OrderCreateDTO(ABBaseDTO):
    order: OrderDataDTO


@dataclass(kw_only=True)
class OrderDetailsDTO(ABBaseDTO):
    order: OrderDataDTO = None


@dataclass(kw_only=True)
class OrderListDTO(ABBaseDTO):
    orders: list[OrderDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class OrderCancelResponseDTO(ABBaseDTO):
    eventUuid: str = None
