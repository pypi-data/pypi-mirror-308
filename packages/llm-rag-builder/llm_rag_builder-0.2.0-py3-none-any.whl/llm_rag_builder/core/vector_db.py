from abc import ABC, abstractmethod
from .vectorizer import BaseVectorizer


class BaseVectorDB(ABC):
    vectorizer: BaseVectorizer

    def __init__(self, vectorizer: BaseVectorizer):
        self.vectorizer = vectorizer

    @abstractmethod
    def insert(self, uuid: str, text: str, meta: dict) -> None:
        """Insert data into the database."""
        pass

    @abstractmethod
    def bulk_insert(self, data: list[dict]) -> None:
        """Insert multiple data entries into the database."""
        pass

    @abstractmethod
    def query(self, query: list[float], num_results: int) -> list[dict]:
        """
        Query the database with the given query and return the results.
        :param query: vector representation of the query
        :param num_results: number of results to return
        :return: list of results
        """
        pass
