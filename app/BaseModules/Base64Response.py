from pydantic import BaseModel, Field


class Base64Response(BaseModel):
    title: str
    filetype: str = Field(default="base64")
    file: str
