import qbittorrentapi
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from data import config


class UserStates(StatesGroup):
    main_menu = State()


async def add_torrent(client: qbittorrentapi.Client, magnet_link: str) -> bool:
    return await client.torrents.add(urls=magnet_link) == 'Ok.'


# noinspection PyShadowingNames
async def on_startup(dp: Dispatcher):
    qbt_client = qbittorrentapi.Client(**config.qbittorrentapi_config)
    dp['qbt'] = qbt_client
    import middlewares
    import filters
    import handlers
    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    handlers.user.setup(dp)


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    executor.start_polling(dp, on_startup=on_startup)
