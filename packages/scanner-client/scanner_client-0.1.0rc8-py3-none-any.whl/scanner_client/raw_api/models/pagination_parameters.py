from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaginationParameters")


@_attrs_define
class PaginationParameters:
    """
    Attributes:
        page_size (Union[Unset, int]):  Default: 50.
        page_token (Union[None, Unset, int]):
    """

    page_size: Union[Unset, int] = 50
    page_token: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        page_size = self.page_size

        page_token: Union[None, Unset, int]
        if isinstance(self.page_token, Unset):
            page_token = UNSET
        else:
            page_token = self.page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if page_size is not UNSET:
            field_dict["page_size"] = page_size
        if page_token is not UNSET:
            field_dict["page_token"] = page_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        page_size = d.pop("page_size", UNSET)

        def _parse_page_token(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        page_token = _parse_page_token(d.pop("page_token", UNSET))

        pagination_parameters = cls(
            page_size=page_size,
            page_token=page_token,
        )

        pagination_parameters.additional_properties = d
        return pagination_parameters

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
