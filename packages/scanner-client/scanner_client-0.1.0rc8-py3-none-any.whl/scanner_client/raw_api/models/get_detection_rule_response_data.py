from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.detection_rule import DetectionRule


T = TypeVar("T", bound="GetDetectionRuleResponseData")


@_attrs_define
class GetDetectionRuleResponseData:
    """
    Attributes:
        detection_rule (DetectionRule):
    """

    detection_rule: "DetectionRule"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        detection_rule = self.detection_rule.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "detection_rule": detection_rule,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.detection_rule import DetectionRule

        d = src_dict.copy()
        detection_rule = DetectionRule.from_dict(d.pop("detection_rule"))

        get_detection_rule_response_data = cls(
            detection_rule=detection_rule,
        )

        get_detection_rule_response_data.additional_properties = d
        return get_detection_rule_response_data

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
