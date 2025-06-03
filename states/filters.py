from aiogram.filters import BaseFilter
from aiogram.types import Message


class NotCancelFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.strip() != "❌ Отмена"
