from ...core import BaseLLM, BaseVectorDB, BaseVectorizer

try:
    from yandex_chain import ChatYandexGPT
    from langchain.schema import AIMessage, HumanMessage, SystemMessage

except ImportError as e:
    print(e)
    print("Yandex library not found. Please install it using 'pip install yandex-chain'")
    exit()


class YandexLLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer

    api_key: str
    catalog_id: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: ChatYandexGPT

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,
        catalog_id,

        prepare_model='yandexgpt',
        prepare_prompt='',

        llm_model='yandexgpt',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key
        self.catalog_id = catalog_id

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model

        self.client = ChatYandexGPT(api_key=self.api_key, folder_id=self.catalog_id)

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list | None) -> str:
        msgs = []
        for message in messages:
            match message.role:
                case 'system':
                    msgs.append(SystemMessage(content="Системное сообщение: " + message['content']))
                case 'user':
                    msgs.append(HumanMessage(content=message['content']))
                case 'agent':
                    msgs.append(AIMessage(content=message['content']))
                case _:
                    msgs.append(AIMessage(content=message['content']))

        langchain_result = self.client([
            *msgs
        ])

        return langchain_result.content
