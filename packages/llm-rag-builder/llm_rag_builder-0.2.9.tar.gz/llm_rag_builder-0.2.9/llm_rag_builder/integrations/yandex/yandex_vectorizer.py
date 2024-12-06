from ...core import BaseVectorizer

try:
    from yandex_chain import YandexEmbeddings

except ImportError as e:
    print(e)
    print("Yandex library not found. Please install it using 'pip install yandex-chain'")
    exit()


class YandexVectorizer(BaseVectorizer):
    api_key: str
    catalog_id: str
    dimensions: int = 256
    embeddings: YandexEmbeddings

    def __init__(self, api_key, catalog_id):
        self.api_key = api_key
        self.catalog_id = catalog_id
        self.embeddings = YandexEmbeddings(api_key=self.api_key, folder_id=self.catalog_id)

    def vectorize(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)

    def bulk_vectorize(self, texts: list[str]) -> list[list[float]]:
        vector = []
        for text in texts:
            vector.append(self.embeddings.embed_query(text))
        return vector
