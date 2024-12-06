from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.create_event_sink_request_data import CreateEventSinkRequestData


T = TypeVar("T", bound="CrudApiRequestAndResponseDataForEventSinkApiHandlerType2")


@_attrs_define
class CrudApiRequestAndResponseDataForEventSinkApiHandlerType2:
    """
    Attributes:
        create_req (CreateEventSinkRequestData):
    """

    create_req: "CreateEventSinkRequestData"

    def to_dict(self) -> Dict[str, Any]:
        create_req = self.create_req.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "CreateReq": create_req,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_event_sink_request_data import CreateEventSinkRequestData

        d = src_dict.copy()
        create_req = CreateEventSinkRequestData.from_dict(d.pop("CreateReq"))

        crud_api_request_and_response_data_for_event_sink_api_handler_type_2 = cls(
            create_req=create_req,
        )

        return crud_api_request_and_response_data_for_event_sink_api_handler_type_2
