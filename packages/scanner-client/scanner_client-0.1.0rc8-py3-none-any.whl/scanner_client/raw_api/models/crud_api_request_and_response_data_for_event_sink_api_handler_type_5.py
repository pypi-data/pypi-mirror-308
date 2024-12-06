from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_event_sink_request_data import UpdateEventSinkRequestData


T = TypeVar("T", bound="CrudApiRequestAndResponseDataForEventSinkApiHandlerType5")


@_attrs_define
class CrudApiRequestAndResponseDataForEventSinkApiHandlerType5:
    """
    Attributes:
        update_req (UpdateEventSinkRequestData):
    """

    update_req: "UpdateEventSinkRequestData"

    def to_dict(self) -> Dict[str, Any]:
        update_req = self.update_req.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "UpdateReq": update_req,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_event_sink_request_data import UpdateEventSinkRequestData

        d = src_dict.copy()
        update_req = UpdateEventSinkRequestData.from_dict(d.pop("UpdateReq"))

        crud_api_request_and_response_data_for_event_sink_api_handler_type_5 = cls(
            update_req=update_req,
        )

        return crud_api_request_and_response_data_for_event_sink_api_handler_type_5
