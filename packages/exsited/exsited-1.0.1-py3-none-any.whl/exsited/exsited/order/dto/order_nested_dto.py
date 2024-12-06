from dataclasses import dataclass
from exsited.exsited.common.dto.common_dto import TaxDTO
from exsited.sdlize.ab_base_dto import ABBaseDTO


@dataclass(kw_only=True)
class OrderItemAccountingCodeDTO(ABBaseDTO):
    salesRevenue: str = None


@dataclass(kw_only=True)
class OrderItemPricingRuleDTO(ABBaseDTO):
    price: str
    uuid: str = None
    price: str = None
    version: str = None
    priceType: str = None
    uom: str = None
    pricePeriod: str = None
    pricingSchedule: str = None
    pricingLevel: str = None
    pricingMethod: str = None
    warehouse: str = None


@dataclass(kw_only=True)
class OrderItemSaleTaxConfigurationDTO(ABBaseDTO):
    salePriceIsBasedOn: str = None
    taxCode: TaxDTO = None


@dataclass(kw_only=True)
class OrderItemPriceSnapshotDTO(ABBaseDTO):
    pricingRule: OrderItemPricingRuleDTO = None

    def add_rule(self, price: str):
        self.pricingRule = OrderItemPricingRuleDTO(price=price)
        return self


@dataclass(kw_only=True)
class POInformationDTO(ABBaseDTO):
    id: str = None
    name: str = None
    accountId: str = None
    currency: str = None
    itemQuantity: str = None
    itemPriceSnapshot: OrderItemPriceSnapshotDTO = None


@dataclass(kw_only=True)
class OrderPurchaseDTO(ABBaseDTO):
    createPo: str = None
    poInformation: POInformationDTO = None


@dataclass(kw_only=True)
class OrderLineDTO(ABBaseDTO):
    itemId: str = None
    itemOrderQuantity: str
    itemUuid: str = None
    itemName: str = None
    shippingCost: str = None
    itemInvoiceNote: str = None
    itemDescription: str = None
    itemType: str = None
    itemChargeType: str = None
    chargeItemUuid: str = None
    version: str = None
    itemPriceTax: TaxDTO = None
    isTaxExemptWhenSold: str = None
    itemAccountingCode: OrderItemAccountingCodeDTO = None
    itemPriceSnapshot: OrderItemPriceSnapshotDTO = None
    itemSaleTaxConfiguration: OrderItemSaleTaxConfigurationDTO = None
    purchaseOrder: OrderPurchaseDTO = None


@dataclass(kw_only=True)
class OrderPropertiesDTO(ABBaseDTO):
    communicationProfile: str = None
    invoiceMode: str = None
    invoiceTerm: str = None
    billingPeriod: str = None
    paymentProcessor: str = None
    paymentMode: str = None
    paymentTerm: str = None
    paymentTermAlignment: str = None
    fulfillmentMode: str = None
    fulfillmentTerm: str = None
