from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.delete_event_sink_request_data import DeleteEventSinkRequestData


T = TypeVar("T", bound="CrudApiRequestAndResponseDataForEventSinkApiHandlerType6")


@_attrs_define
class CrudApiRequestAndResponseDataForEventSinkApiHandlerType6:
    """
    Attributes:
        delete_req (DeleteEventSinkRequestData):
    """

    delete_req: "DeleteEventSinkRequestData"

    def to_dict(self) -> Dict[str, Any]:
        delete_req = self.delete_req.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "DeleteReq": delete_req,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.delete_event_sink_request_data import DeleteEventSinkRequestData

        d = src_dict.copy()
        delete_req = DeleteEventSinkRequestData.from_dict(d.pop("DeleteReq"))

        crud_api_request_and_response_data_for_event_sink_api_handler_type_6 = cls(
            delete_req=delete_req,
        )

        return crud_api_request_and_response_data_for_event_sink_api_handler_type_6
