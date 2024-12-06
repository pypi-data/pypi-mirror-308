from ...core import BaseLLM, BaseVectorDB, BaseVectorizer, BaseMessage

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError as e:
    print(e)
    print("google-generativeai library not found. Please install it using 'pip install -q -U google-generativeai'")
    exit()


class GeminiLLM(BaseLLM):  # noqa
    db: BaseVectorDB
    vectorizer: BaseVectorizer

    api_key: str

    prepare_model: str
    prepare_prompt: str

    llm_model: str
    client: genai.GenerativeModel

    def __init__(
        self,
        db: BaseVectorDB,
        vectorizer: BaseVectorizer,

        api_key,

        prepare_model='gemini-1.5-flash',
        prepare_prompt='',

        llm_model='gemini-1.5-flash',
    ):
        super().__init__(db, vectorizer)
        self.api_key = api_key

        self.prepare_model = prepare_model
        self.prepare_prompt = prepare_prompt

        self.llm_model = llm_model
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(
            self.llm_model,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

        )

    def prepare_query(self, query: str) -> str:
        return query

    def generate_response(self, messages: list[BaseMessage] | None) -> str:
        msgs = []
        for msg in messages:
            match msg.role:
                case 'user':
                    msgs.append({"role": "user", "content": msg.content})
                case 'system':
                    msgs.append({"role": "system", "content": "SYSTEM INFO: " + msg.content})
                case 'agent':
                    msgs.append({"role": "assistant", "content": msg.content})

        chat = self.client.start_chat(
            history=msgs[:-1],
        )
        return chat.send_message(msgs[-1]).text
