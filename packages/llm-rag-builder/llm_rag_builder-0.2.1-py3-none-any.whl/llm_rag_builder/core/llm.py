from abc import ABC, abstractmethod
from .vector_db import BaseVectorDB
from .vectorizer import BaseVectorizer


class BaseLLM(ABC):
    db: BaseVectorDB
    vectorizer: BaseVectorizer

    def __init__(self, db: BaseVectorDB, vectorizer: BaseVectorizer):
        self.db = db
        self.vectorizer = vectorizer

    def vectorize(self, text: str) -> list[float]:
        """Convert input text to its vector representation."""
        return self.vectorizer.vectorize(text)

    def prepare_query(self, query: str) -> str:
        """Prepare the input query for searching."""
        return query

    def search_query(self, query: str, num_results: int) -> list[dict]:
        """Search the query in the vector database."""
        query = self.prepare_query(query)
        vector = self.vectorize(query)
        return self.db.query(vector, num_results)

    @abstractmethod
    def generate_response(self, messages: list | None) -> str:
        """Generate a response for the query."""
        pass
