from exsited.exsited.payment.dto.payment_dto import PaymentDetailsDTO, PaymentCreateDTO, CardPaymentCreateDTO, \
    CardDirectDebitPaymentCreateDTO
from exsited.exsited.payment.payment_api_url import PaymentApiUrl
from exsited.common.sdk_util import SDKUtil
from exsited.http.ab_rest_processor import ABRestProcessor

class Payment(ABRestProcessor):

    def create(self, invoice_id: str, request_data: PaymentCreateDTO) -> PaymentDetailsDTO:
        response = self.post(url=PaymentApiUrl.PAYMENT_CREATE.format(invoice_id=invoice_id), request_obj=request_data, response_obj=PaymentDetailsDTO())
        return response

    def create_card(self, invoice_id: str, request_data: CardPaymentCreateDTO) -> PaymentDetailsDTO:
        response = self.post(url=PaymentApiUrl.PAYMENT_CREATE_CARD.format(invoice_id=invoice_id), request_obj=request_data, response_obj=PaymentDetailsDTO())
        return response

    def create_direct_debit(self, invoice_id: str, request_data: CardDirectDebitPaymentCreateDTO) -> PaymentDetailsDTO:
        response = self.post(url=PaymentApiUrl.PAYMENT_CREATE_DIRECT_DEBIT.format(invoice_id=invoice_id),
                             request_obj=request_data, response_obj=PaymentDetailsDTO())
        return response
