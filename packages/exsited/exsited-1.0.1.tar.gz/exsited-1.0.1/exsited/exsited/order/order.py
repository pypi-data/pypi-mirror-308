from exsited.exsited.common.common_enum import SortDirection
from exsited.exsited.order.dto.order_dto import OrderCreateDTO, OrderDetailsDTO, OrderListDTO, OrderCancelResponseDTO
from exsited.exsited.order.dto.usage_dto import UsageCreateDTO, UsageDataDTO
from exsited.exsited.order.order_api_url import OrderApiUrl
from exsited.common.sdk_util import SDKUtil
from exsited.http.ab_rest_processor import ABRestProcessor


class Order(ABRestProcessor):

    def create(self, request_data: OrderCreateDTO) -> OrderDetailsDTO:
        response = self.post(url=OrderApiUrl.ORDERS, request_obj=request_data, response_obj=OrderDetailsDTO())
        return response

    def list(self, limit: int = None, offset: int = None, direction: SortDirection = None, order_by: str = None) -> OrderListDTO:
        params = SDKUtil.init_pagination_params(limit=limit, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=OrderApiUrl.ORDERS, params=params, response_obj=OrderListDTO())
        return response

    def details(self, id: str) -> OrderDetailsDTO:
        response = self.get(url=OrderApiUrl.ORDERS + f"/{id}", response_obj=OrderDetailsDTO())
        return response

    def cancel(self, id: str, effective_date: str) -> OrderCancelResponseDTO:
        response = self.post(url=OrderApiUrl.ORDER_CANCEL.format(id=id), json_dict={"order": {"effective_date": effective_date}}, response_obj=OrderCancelResponseDTO())
        return response

    def add_usage(self, request_data: UsageCreateDTO) -> UsageDataDTO:
        response = self.post(url=OrderApiUrl.USAGE_ADD, request_obj=request_data, response_obj=UsageCreateDTO())
        return response

    def create_with_purchase(self, request_data: OrderCreateDTO) -> OrderDetailsDTO:
        response = self.post(url=OrderApiUrl.PURCHASE_ORDER_CREATE, request_obj=request_data, response_obj=OrderDetailsDTO())
        return response
