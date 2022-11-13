from pydantic import BaseModel


class AbstractBotModel(BaseModel):
    ...


class Massage(AbstractBotModel):
    chat: dict
    text: str


class BotUpdates(AbstractBotModel):
    update_id: int
    message: Massage


class BotMessage(AbstractBotModel):
    chat_id: int
    text: str


class BotConfig(BaseModel):
    headers: dict
