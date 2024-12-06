from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.webhook_configuration import WebhookConfiguration


T = TypeVar("T", bound="IntegrationConfigurationType3")


@_attrs_define
class IntegrationConfigurationType3:
    """
    Attributes:
        webhook (WebhookConfiguration): Represents configuration to send messages to a webhook.
    """

    webhook: "WebhookConfiguration"

    def to_dict(self) -> Dict[str, Any]:
        webhook = self.webhook.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "Webhook": webhook,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.webhook_configuration import WebhookConfiguration

        d = src_dict.copy()
        webhook = WebhookConfiguration.from_dict(d.pop("Webhook"))

        integration_configuration_type_3 = cls(
            webhook=webhook,
        )

        return integration_configuration_type_3
