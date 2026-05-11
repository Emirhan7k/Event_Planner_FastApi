class EmbeddingService:
    def embed_text(self, text: str) -> list[float]:
        tokens = text.lower().split()
        return [float(len(token)) / 10 for token in tokens[:16]]


embedding_service = EmbeddingService()
