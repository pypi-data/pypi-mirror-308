from ...core import BaseLLM, BaseVectorDB, BaseVectorizer, BaseMessage

try:
    import openai
except ImportError as e:
    print(e)
    print("OpenAI library not found. Please install it using 'pip install openai'")
    exit()


class OpenAILLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer

    api_key: str
    base_url: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: openai.Client

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,
        base_url='https://api.openai.com/v1',

        prepare_model='gpt-3.5-turbo',
        prepare_prompt='',

        llm_model='gpt-3.5-turbo',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key
        self.base_url = base_url

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model
        self.client = openai.Client(api_key=self.api_key, base_url=self.base_url)

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list[BaseMessage] | None) -> str:
        msgs = []
        for message in messages:
            match message.role:
                case 'user':
                    msgs.append({"role": "user", "content": message.content})
                case 'system':
                    msgs.append({"role": "system", "content": "SYSTEM INFO:\n" + message.content})
                case 'agent':
                    msgs.append({"role": "assistant", "content": message.content})

        response = self.client.chat.completions.create(
            messages=msgs,
            model=self.llm_model,
        )
        return response.choices[0].message.content
