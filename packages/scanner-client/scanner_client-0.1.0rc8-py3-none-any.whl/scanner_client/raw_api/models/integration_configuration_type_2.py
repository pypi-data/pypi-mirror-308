from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.tines_configuration import TinesConfiguration


T = TypeVar("T", bound="IntegrationConfigurationType2")


@_attrs_define
class IntegrationConfigurationType2:
    """
    Attributes:
        tines (TinesConfiguration):
    """

    tines: "TinesConfiguration"

    def to_dict(self) -> Dict[str, Any]:
        tines = self.tines.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "Tines": tines,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tines_configuration import TinesConfiguration

        d = src_dict.copy()
        tines = TinesConfiguration.from_dict(d.pop("Tines"))

        integration_configuration_type_2 = cls(
            tines=tines,
        )

        return integration_configuration_type_2
