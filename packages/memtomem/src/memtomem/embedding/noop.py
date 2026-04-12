"""No-op embedding provider for BM25-only mode."""

from __future__ import annotations

from typing import Sequence


class NoopEmbedder:
    """Embedding provider that returns empty vectors.

    Used when no embedding backend is configured (``provider="none"``).
    The search pipeline falls back to BM25-only keyword search, and the
    index engine skips vector storage entirely.
    """

    @property
    def dimension(self) -> int:
        return 0

    @property
    def model_name(self) -> str:
        return "none"

    async def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        return [[] for _ in texts]

    async def embed_query(self, query: str) -> list[float]:
        return []

    async def close(self) -> None:
        pass
