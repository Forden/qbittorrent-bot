from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data import config


class AccessFilterMiddleware(BaseMiddleware):

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    async def on_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in config.admins:
            raise CancelHandler()
