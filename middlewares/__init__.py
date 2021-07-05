from aiogram import Dispatcher

from .access_filter import AccessFilterMiddleware
from .qbt_client import QBittorrentClient


def setup(dp: Dispatcher):
    dp.middleware.setup(AccessFilterMiddleware())
    dp.middleware.setup(QBittorrentClient(dp['qbt']))
