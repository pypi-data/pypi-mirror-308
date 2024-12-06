from abc import ABC, abstractmethod


class BaseVectorizer(ABC):
    dimensions: int

    @abstractmethod
    def vectorize(self, text: str) -> list[float]:
        """Convert input text to its vector representation."""
        pass

    @abstractmethod
    def bulk_vectorize(self, texts: list[str]) -> list[list[float]]:
        """Convert input texts to their vector representations."""
        pass
