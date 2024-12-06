from exsited.exsited.common.common_enum import SortDirection
from exsited.exsited.purchase_order.dto.purchase_order_dto import PurchaseOrderDetailsDTO, PurchaseOrderListDTO
from exsited.exsited.purchase_order.purchase_order_api_url import PurchaseOrderApiUrl
from exsited.common.sdk_util import SDKUtil
from exsited.http.ab_rest_processor import ABRestProcessor


class PurchaseOrder(ABRestProcessor):

    def list(self, limit: int = None, offset: int = None, direction: SortDirection = None, order_by: str = None) -> PurchaseOrderListDTO:
        params = SDKUtil.init_pagination_params(limit=limit, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=PurchaseOrderApiUrl.PURCHASE_ORDERS, params=params, response_obj=PurchaseOrderListDTO())
        return response

    def details(self, id: str) -> PurchaseOrderDetailsDTO:
        response = self.get(url=PurchaseOrderApiUrl.PURCHASE_ORDER_DETAILS.format(id=id), response_obj=PurchaseOrderDetailsDTO())#PurchaseOrderDetailsDTO()
        return response
