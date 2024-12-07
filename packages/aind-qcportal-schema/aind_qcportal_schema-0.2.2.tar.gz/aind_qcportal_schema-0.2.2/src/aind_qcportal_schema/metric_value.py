from pydantic import BaseModel, Field, model_validator
from typing import Any, Optional
from aind_data_schema.core.quality_control import Status


class DropdownMetric(BaseModel):
    """Dropdown metric schema

    Renders as: https://panel.holoviz.org/reference/widgets/Select.html
    """

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: str = "dropdown"


class CheckboxMetric(BaseModel):
    """Checkbox metric schema

    Renders as: https://panel.holoviz.org/reference/widgets/Checkbox.html
    """

    value: Any = Field(..., title="Value")
    options: list[Any] = Field(..., title="Options")
    status: Optional[list[Status]] = Field(default=None, title="Option to status mapping")
    type: str = "checkbox"


class RulebasedMetric(BaseModel):
    """Rulebased metric schema"""

    value: Any = Field(..., title="Value")
    rule: str = Field(..., title="Runs eval(rule), Status.PASS when true, Status.FAIL when false")


class MultiAssetMetric(BaseModel):
    """Multi-asset metric schema"""

    values: list[Any] = Field(..., title="Values", description="Length should match evaluated_assets. Use only basic types (str, int, float, bool)")
    options: Optional[list[Any]] = Field(default=None, title="Options")
    type: Optional[str] = Field(default=None, title="Type", description="Set to 'dropdown' or 'checkbox' if you included options")

    @model_validator(mode="after")
    def validate_type_if_options(cls, v):
        if v.options is not None and v.type is None:
            raise ValueError("Type must be set if options are included")

        return v
