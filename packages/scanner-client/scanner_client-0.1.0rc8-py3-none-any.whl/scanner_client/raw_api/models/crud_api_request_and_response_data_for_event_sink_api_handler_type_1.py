from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.list_response_with_pagination_for_list_event_sinks_response_data import (
        ListResponseWithPaginationForListEventSinksResponseData,
    )


T = TypeVar("T", bound="CrudApiRequestAndResponseDataForEventSinkApiHandlerType1")


@_attrs_define
class CrudApiRequestAndResponseDataForEventSinkApiHandlerType1:
    """
    Attributes:
        list_resp (ListResponseWithPaginationForListEventSinksResponseData):
    """

    list_resp: "ListResponseWithPaginationForListEventSinksResponseData"

    def to_dict(self) -> Dict[str, Any]:
        list_resp = self.list_resp.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "ListResp": list_resp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_response_with_pagination_for_list_event_sinks_response_data import (
            ListResponseWithPaginationForListEventSinksResponseData,
        )

        d = src_dict.copy()
        list_resp = ListResponseWithPaginationForListEventSinksResponseData.from_dict(d.pop("ListResp"))

        crud_api_request_and_response_data_for_event_sink_api_handler_type_1 = cls(
            list_resp=list_resp,
        )

        return crud_api_request_and_response_data_for_event_sink_api_handler_type_1
