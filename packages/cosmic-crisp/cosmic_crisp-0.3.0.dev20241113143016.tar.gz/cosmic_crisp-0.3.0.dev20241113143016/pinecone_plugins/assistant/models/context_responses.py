from dataclasses import dataclass
from typing import TypeVar, Union

from pinecone_plugins.assistant.data.core.client.model.context_model import ContextModel as OpenAPIContextModel
from pinecone_plugins.assistant.data.core.client.model.reference_model import ReferenceModel as OpenAPISnippetModel
from pinecone_plugins.assistant.models.file_model import FileModel
from pinecone_plugins.assistant.models.shared import TokenCounts

RefType = TypeVar("RefType", bound=Union["TextReference", "PdfReference"])
ContentType = TypeVar("ContentType", bound=Union["TextContent"])


@dataclass
class BaseContent:
    @classmethod
    def from_openapi(cls, value):
        raise NotImplementedError


@dataclass
class TextContent(BaseContent):
    text: str

    @classmethod
    def from_openapi(cls, content_dict: dict) -> "TextContent":
        return cls(text=content_dict["text"])


@dataclass
class BaseReference:

    @classmethod
    def from_openapi(cls, value):
        raise NotImplementedError


@dataclass
class TextReference(BaseReference):
    file: FileModel

    @classmethod
    def from_openapi(cls, ref_dict: dict) -> "TextReference":
        return cls(file=FileModel(data=ref_dict["file"]))


@dataclass
class PdfReference(BaseReference):
    pages: list[int]
    file: FileModel

    @classmethod
    def from_openapi(cls, ref_dict: dict) -> "PdfReference":
        return cls(pages=ref_dict["pages"], file=FileModel(data=ref_dict["file"]))


class TypedContent:
    @classmethod
    def from_openapi(cls, d: dict) -> ContentType:
        type_ = d["type"]
        ref_map = {
            "Text": TextContent,
        }
        return ref_map[type_].from_openapi(d)


class TypedReference:
    @classmethod
    def from_openapi(cls, d: dict) -> RefType:
        type_ = d["type"]
        ref_map = {
            "Text": TextReference,
            "Pdf": PdfReference
        }
        return ref_map[type_].from_openapi(d)


@dataclass
class Snippet:
    content: ContentType
    score: float
    reference: RefType

    @classmethod
    def from_openapi(cls, snippet: OpenAPISnippetModel):
        return cls(
            content=TypedContent.from_openapi(snippet.content),
            score=snippet.score,
            reference=TypedReference.from_openapi(snippet.reference)
        )


@dataclass
class ContextResponse:
    snippets: list[Snippet]
    usage: TokenCounts

    @classmethod
    def from_openapi(cls, ctx: OpenAPIContextModel):
        return cls(
            snippets=[Snippet.from_openapi(snippet) for snippet in ctx.snippets],
            usage=TokenCounts.from_openapi(ctx.usage)
        )
