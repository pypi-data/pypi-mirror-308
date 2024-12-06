from dataclasses import dataclass
from exsited.sdlize.ab_base_dto import ABBaseDTO

@dataclass(kw_only=True)
class PaymentAppliedDTO(ABBaseDTO):
    processor: str = None
    amount: float = None
    reference: str = None
    method: str = None

@dataclass(kw_only=True)
class CardPaymentAppliedDTO(PaymentAppliedDTO):
    cardType: str = None
    token: str = None
    cardNumber: str = None
    expiryMonth: str = None
    expiryYear: str = None
    additionalFields: dict = None

@dataclass(kw_only=True)
class CreditAppliedDTO(ABBaseDTO):
    id: str = None
    amount: str = None

@dataclass(kw_only=True)
class InvoiceDTO(ABBaseDTO):
    applied: float = None
    code: str = None
    dueDate: str = None
    issueDate: str = None
    outstanding: float = None
    total: float = None

@dataclass(kw_only=True)
class PaymentDataDTO(ABBaseDTO):
    id: str = None
    date: str = None
    status: str = None
    reconcileStatus: str = None
    totalApplied: float = None
    paymentApplied: list[PaymentAppliedDTO] = None
    note: str = None
    creditApplied: list[CreditAppliedDTO] = None
    invoices: list[InvoiceDTO] = None
    createdBy: str = None
    createdOn: str = None
    lastUpdatedBy: str = None
    lastUpdatedOn: str = None
    uuid: str = None
    version: str = None
    customAttributes: list = None
    customObjects: list = None


@dataclass(kw_only=True)
class CardPaymentDataDTO(PaymentDataDTO):
    paymentApplied: list[CardPaymentAppliedDTO] = None

@dataclass(kw_only=True)
class PaymentDetailsDTO(ABBaseDTO):
    payment: PaymentDataDTO = None

@dataclass(kw_only=True)
class PaymentCreateDTO(ABBaseDTO):
    payment: PaymentDataDTO

@dataclass(kw_only=True)
class CardPaymentCreateDTO(ABBaseDTO):
    payment: CardPaymentDataDTO

# New DTO for the given payload
@dataclass(kw_only=True)
class CardDirectDebitPaymentAppliedDTO(PaymentAppliedDTO):
    method: str = None

@dataclass(kw_only=True)
class CardDirectDebitPaymentDataDTO(ABBaseDTO):
    date: str = None
    paymentApplied: list[CardDirectDebitPaymentAppliedDTO] = None

@dataclass(kw_only=True)
class CardDirectDebitPaymentCreateDTO(ABBaseDTO):
    payment: CardDirectDebitPaymentDataDTO
