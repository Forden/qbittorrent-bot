import qbittorrentapi
from aiogram import types

import keyboards.default
import states.user
from utils.misc.torrent_state_utils import state_emojis


async def my_torrents(msg: types.Message, qbt: qbittorrentapi.Client):
    torrents = qbt.torrents.info()
    m = [
        'Торренты:',
        ''
    ]
    names = []
    for i, info in enumerate(sorted(torrents, key=lambda k: k['state'])):
        m.append(
            f'{i}) - {info["name"]} {state_emojis[info["state"]]}',
        )
        m.append('')
        names.append(info['name'])
    await msg.answer('\n'.join(m), reply_markup=keyboards.default.MainMenu.torrents_list(names))
    await states.user.MainMenu.choosing_torrent.set()
