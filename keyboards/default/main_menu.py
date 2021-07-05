from typing import List

import qbittorrentapi

from .consts import DefaultConstructor


class MainMenu(DefaultConstructor):
    @staticmethod
    def main_menu():
        schema = [2]
        actions = [
            '📖Мои торренты',
            '➕Добавить торрент'
        ]
        return MainMenu._create_kb(actions, schema)

    @staticmethod
    def torrents_list(torrents: List[str]):
        schema = [1]
        btns = ['◀️В меню']
        for i in torrents:
            schema.append(1)
            btns.append(i)
        return MainMenu._create_kb(btns, schema)

    @staticmethod
    def torrent_data(torrent_data: qbittorrentapi.TorrentDictionary):
        schema = [2]
        btns = [
            '◀️Мои торренты',
            '🔄Обновить',
        ]
        if torrent_data.state_enum.is_paused:
            schema.append(1)
            btns.append('▶️Возобновить')
        elif torrent_data.state_enum.is_uploading or torrent_data.state_enum.is_downloading:
            schema.append(1)
            btns.append('⏸Приостановить')
        if torrent_data['state'] == 'pausedUP':
            schema.append(1)
            btns.append('❗️▶️Возобновить принудительно')
        schema.append(1)
        btns.append('🧲Magnet')
        schema.extend([1, 1, 1])
        btns.extend([
            '🔎Перепроверить принудительно',
            '🔎Переанонсировать принудительно',
            '✏️Переименовать торрент'
        ])
        return MainMenu._create_kb(btns, schema)
