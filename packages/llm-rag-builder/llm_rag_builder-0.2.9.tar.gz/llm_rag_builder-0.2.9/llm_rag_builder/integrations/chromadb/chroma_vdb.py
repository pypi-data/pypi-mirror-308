from ...core import BaseVectorDB, BaseVectorizer

try:
    import chromadb
    from chromadb import Documents, EmbeddingFunction
except ImportError:
    print("Chroma library not found. Please install it using 'pip install chromadb'")
    exit()


class ChromaVDBMixin(BaseVectorDB):
    client: chromadb.ClientAPI
    chunks_collection: chromadb.Collection

    def insert(self, uuid: str, text: str, meta: dict) -> None:
        self.chunks_collection.add(
            documents=[text],
            embeddings=[self.vectorizer.vectorize(text)],
            metadatas=[meta],
            ids=[uuid],
        )

    def bulk_insert(self, data: list[dict]) -> None:
        data = [d for d in data if d['text']]
        documents = [d['text'] for d in data]
        metadatas = [d['meta'] for d in data]
        ids = [d['uuid'] for d in data]

        self.chunks_collection.add(
            documents=documents,
            embeddings=self.vectorizer.bulk_vectorize(documents),
            metadatas=metadatas,
            ids=ids,
        )

    def query(self, query: list[float], num_results: int, where=None) -> list[dict]:
        results = self.chunks_collection.query(
            query_embeddings=query,
            n_results=num_results,
            where=where,
        )

        response = []
        for uuid, text in zip(results['ids'][0], results['documents'][0]):
            response.append({'uuid': uuid, 'text': text})

        return response


class PersistentChromaVDB(ChromaVDBMixin):
    def __init__(self, vectorizer: BaseVectorizer, path: str = "vdb.chromadb"):
        super().__init__(vectorizer)
        self.client = chromadb.PersistentClient(path=path)

        class CustomEmbeddingFunction(EmbeddingFunction):
            def __call__(self, input: Documents) -> list[list[float]]:
                embeddings = vectorizer.bulk_vectorize(input)
                return embeddings

        self.chunks_collection = self.client.get_or_create_collection(name='chunks', embedding_function=CustomEmbeddingFunction())
