from typing import TYPE_CHECKING, Any, Dict, Type, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.create_slack_integration_args import CreateSlackIntegrationArgs


T = TypeVar("T", bound="CreateIntegrationArgsType0")


@_attrs_define
class CreateIntegrationArgsType0:
    """
    Attributes:
        slack (CreateSlackIntegrationArgs):
    """

    slack: "CreateSlackIntegrationArgs"

    def to_dict(self) -> Dict[str, Any]:
        slack = self.slack.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "Slack": slack,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_slack_integration_args import CreateSlackIntegrationArgs

        d = src_dict.copy()
        slack = CreateSlackIntegrationArgs.from_dict(d.pop("Slack"))

        create_integration_args_type_0 = cls(
            slack=slack,
        )

        return create_integration_args_type_0
