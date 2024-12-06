from dataclasses import dataclass
from pinecone_plugins.assistant.evaluation.core.client.model.token_counts import TokenCounts as OpenAPITokenCounts


@dataclass
class TokenCounts:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    @classmethod
    def from_openapi(cls, token_counts: OpenAPITokenCounts):
        return cls(
            prompt_tokens=token_counts.prompt_tokens,
            completion_tokens=token_counts.completion_tokens,
            total_tokens=token_counts.total_tokens
        )