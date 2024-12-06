from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.update_webhook_integration_args import UpdateWebhookIntegrationArgs


T = TypeVar("T", bound="UpdateIntegrationArgsType1")


@_attrs_define
class UpdateIntegrationArgsType1:
    """
    Attributes:
        webhook (UpdateWebhookIntegrationArgs):
    """

    webhook: "UpdateWebhookIntegrationArgs"

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
        from ..models.update_webhook_integration_args import UpdateWebhookIntegrationArgs

        d = src_dict.copy()
        webhook = UpdateWebhookIntegrationArgs.from_dict(d.pop("Webhook"))

        update_integration_args_type_1 = cls(
            webhook=webhook,
        )

        return update_integration_args_type_1
