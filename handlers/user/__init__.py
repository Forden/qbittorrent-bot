from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

import states.user
from filters import MultiRegexp
from .magnet_catcher import catcher, start_adding_torrent
from .my_torrents import my_torrents
from .start import bot_start
from .torrent_data import (
    force_start_torrent, get_magnet_url, get_torrent_data, pause_torrent, reannounce_torrent, recheck_torrent,
    resume_torrent, set_torrent_name, start_renaming_torrent, update_torrent_data
)


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart(), state='*')
    dp.register_message_handler(bot_start, text=['◀️В меню'], state='*')
    dp.register_message_handler(bot_start, state=None)

    dp.register_message_handler(start_adding_torrent, text=['➕Добавить торрент'], state=states.user.MainMenu.main_menu)
    dp.register_message_handler(
        catcher, MultiRegexp(r"(magnet:\?xt[=\w\:\&\;\+\%-.]+)"), state=states.user.AddingTorrent.insert_links
    )
    dp.register_message_handler(my_torrents, text=['📖Мои торренты'], state=states.user.MainMenu.main_menu)
    dp.register_message_handler(my_torrents, text=['◀️Мои торренты'], state=states.user.MainMenu.inspecting_torrent)
    dp.register_message_handler(get_torrent_data, state=states.user.MainMenu.choosing_torrent)
    dp.register_message_handler(update_torrent_data, text=['🔄Обновить'], state=states.user.MainMenu.inspecting_torrent)
    dp.register_message_handler(
        pause_torrent, text=['⏸Приостановить'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        resume_torrent, text=['▶️Возобновить'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        force_start_torrent, text=['❗️▶️Возобновить принудительно'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        reannounce_torrent, text=['🔎Переанонсировать принудительно'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        recheck_torrent, text=['🔎Перепроверить принудительно'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        get_magnet_url, text=['🧲Magnet'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        start_renaming_torrent, text=['✏️Переименовать торрент'], state=states.user.MainMenu.inspecting_torrent
    )
    dp.register_message_handler(
        set_torrent_name, state=states.user.MainMenu.rename_torrent
    )
