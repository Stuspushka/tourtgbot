from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Any, Dict, Awaitable
from settings import ALLOWED_USERS


class AccessMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id

        if user_id not in ALLOWED_USERS:
            if isinstance(event, Message):
                await event.answer("❌ У вас нет доступа.")
            elif isinstance(event, CallbackQuery):
                await event.answer("❌ У вас нет доступа.", show_alert=True)
            return

        return await handler(event, data)
