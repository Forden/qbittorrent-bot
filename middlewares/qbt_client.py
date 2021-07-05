import qbittorrentapi
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class QBittorrentClient(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, client: qbittorrentapi.Client):
        super().__init__()
        self.client = client

    async def pre_process(self, obj, data, *args):
        data["qbt"] = self.client

    async def post_process(self, obj, data, *args):
        del data["qbt"]
