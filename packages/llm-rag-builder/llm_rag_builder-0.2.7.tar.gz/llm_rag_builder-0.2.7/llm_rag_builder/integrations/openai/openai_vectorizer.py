from ...core import BaseVectorizer

try:
    import openai
except ImportError:
    print("OpenAI library not found. Please install it using 'pip install openai'")
    exit()


class OpenAIVectorizer(BaseVectorizer):
    api_key: str
    base_url: str
    embeddings_model: str
    dimensions: int = 1536
    client: openai.Client

    def __init__(self, api_key, base_url='https://api.openai.com/v1', embeddings_model='text-embedding-3-small'):
        self.api_key = api_key
        self.base_url = base_url
        self.embeddings_model = embeddings_model
        self.client = openai.Client(api_key=self.api_key, base_url=self.base_url)

    def vectorize(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.embeddings_model, input=[text]
        )
        return response.data[0].embedding

    def bulk_vectorize(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                model=self.embeddings_model, input=text
            )
            embeddings.append(response.data[0].embedding)

        return embeddings
