import itertools
from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AudioFile(BaseModel):
    model_config = ConfigDict(json_schema_extra={"type-friendly": "Audio"})
    file: str = Field(
        title="Upload Audio File",
        description="Please select an audio file to upload",
        json_schema_extra={
            "is-file": True,
            "format": "data-url",
            "accept": "audio/*",
        },
    )

    # will be filled later - not part of schema
    filename: str | None = Field(
        None,
        title="Filename",
        description="The name of the audio file",
        json_schema_extra={
            "uiSchema": {"ui:widget": "hidden"},
        },
    )

    # will be filled later - not part of schema
    content: bytes | None = Field(
        None,
        title="Content",
        description="The content of the audio file",
        json_schema_extra={
            "uiSchema": {"ui:widget": "hidden"},
        },
    )


class Table(BaseModel):
    data: List[Dict[str, str]] = Field(
        json_schema_extra={
            "uiSchema": {
                "ui:widget": "hidden",
            },
        }
    )

    @field_validator("data", mode="before")
    def check_data(cls, value):
        # make sure everything is a string
        columns = set()
        value, other = itertools.tee(value)
        for row in value:
            for key, val in row.items():
                if not isinstance(val, str):
                    row[key] = str(val)
            columns.add(tuple(row))

        if len(columns) > 1:
            raise ValueError(f"All rows must have the same columns, got {columns}")

        return other

    def columns(self):
        return list(self.data[0]) if self.data else []

    def is_empty(self):
        return not bool(self.data)

    class Config:
        json_schema_extra = {
            "type-friendly": "Table",
        }
