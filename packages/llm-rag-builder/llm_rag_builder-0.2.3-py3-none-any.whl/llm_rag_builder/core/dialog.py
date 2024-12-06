from abc import ABC

from .llm import BaseLLM
from .command import BaseCommand


class BaseMessage(ABC):
    content: str
    type: str
    hidden: bool = False
    role: str

    def __init__(self, content: str, message_type: str, role: str):
        self.content = content
        self.type = message_type
        self.role = role


class BaseUserMessage(BaseMessage):
    role = "user"

    def __init__(self, content: str, message_type: str):
        super().__init__(
            content=content,
            message_type=message_type,
            role="user"
        )


class BaseAgentMessage(BaseMessage):
    role = "agent"

    def __init__(self, content: str, message_type: str):
        super().__init__(
            content=content,
            message_type=message_type,
            role="agent"
        )


class BaseSystemMesage(BaseMessage):
    role = "system"

    def __init__(self, content: str, message_type: str):
        super().__init__(
            content=content,
            message_type=message_type,
            role="system"
        )


class BaseDialog(ABC):
    default_llm: BaseLLM
    title: str | None
    commands: list[BaseCommand] | None
    _messages: list[BaseMessage] | None

    def __init__(
            self,
            default_llm: BaseLLM,
            title: str = "Untitled dialog",
            commands: list[BaseCommand] | None = None,
    ):
        self.default_llm = default_llm
        self.title = title
        self.commands = commands or []
        self._messages = []

    @property
    def messages(self):
        return self._messages

    def add_message(self, message: BaseMessage) -> None:
        self._messages.append(message)

    def add_user_message(self, content: str, message_type: str) -> None:
        self.add_message(BaseUserMessage(content=content, message_type=message_type))

    def add_agent_message(self, content: str, message_type: str) -> None:
        self.add_message(BaseAgentMessage(content=content, message_type=message_type))

    def add_system_message(self, content: str, message_type: str) -> None:
        self.add_message(BaseSystemMesage(content=content, message_type=message_type))

    def add_command(self, command: BaseCommand) -> None:
        self.commands.append(command)

    def context_list_to_string(self, context_list: list[dict]) -> str:
        return "\n\n".join([context["text"] for context in context_list])

    def generate_agent_message(self, message_type, llm=None) -> BaseAgentMessage:
        llm = llm or self.default_llm
        agent_message = self.default_llm.generate_response(self._messages)
        self.add_agent_message(agent_message, message_type, llm)
        return agent_message

    def proccess_user_message(
            self,
            content: str,
            message_type: str,
            llm: BaseLLM = None,
            reachable=False,
            reach_num=5,
            hide_system_prompt=True
    ) -> None:
        llm = llm or self.default_llm
        self.add_user_message(content, message_type)

        if reachable:
            context_list = self.default_llm.search_query(content, reach_num)
            context_string = self.context_list_to_string(context_list)
            self.add_system_message(context_string, message_type)

        for _ in range(3):
            agent_message = self.generate_agent_message(message_type, llm)

            for command in self.commands:
                if command.check_is_command(agent_message.content):
                    request = agent_message.content
                    agent_message.hidden = hide_system_prompt
                    response = command.run(request)
                    system_content = "REQUEST {}\nSYSTEM RESPONSE:\n{}".format(request, response)
                    self.add_system_message(system_content, message_type)
                    break
            else:
                break

        return self.messages

    def json(self, hidden=False) -> dict:
        return {
            "title": self.title,
            "messages": [
                {"content": message.content, "type": message.type.name, "role": message.role}
                for message in self._messages if not message.hidden or hidden
            ],
        }

    def from_json(self, json) -> None:
        self.title = json["title"] or self.title
        for message in json["messages"]:
            if message["role"] == "user":
                self.add_user_message(message["content"], message["type"])
            elif message["role"] == "agent":
                self.add_agent_message(message["content"], message["type"], self.default_llm)
            elif message["role"] == "system":
                self.add_system_message(message["content"], message["type"])
            else:
                raise ValueError("Invalid message role")
