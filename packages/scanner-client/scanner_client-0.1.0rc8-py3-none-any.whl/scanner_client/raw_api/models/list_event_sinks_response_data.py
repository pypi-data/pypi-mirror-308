from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.event_sink import EventSink


T = TypeVar("T", bound="ListEventSinksResponseData")


@_attrs_define
class ListEventSinksResponseData:
    """
    Attributes:
        event_sinks (List['EventSink']):
    """

    event_sinks: List["EventSink"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        event_sinks = []
        for event_sinks_item_data in self.event_sinks:
            event_sinks_item = event_sinks_item_data.to_dict()
            event_sinks.append(event_sinks_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "event_sinks": event_sinks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.event_sink import EventSink

        d = src_dict.copy()
        event_sinks = []
        _event_sinks = d.pop("event_sinks")
        for event_sinks_item_data in _event_sinks:
            event_sinks_item = EventSink.from_dict(event_sinks_item_data)

            event_sinks.append(event_sinks_item)

        list_event_sinks_response_data = cls(
            event_sinks=event_sinks,
        )

        list_event_sinks_response_data.additional_properties = d
        return list_event_sinks_response_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
