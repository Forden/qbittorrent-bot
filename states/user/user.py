from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    main_menu = State()
    choosing_torrent = State()
    inspecting_torrent = State()
    rename_torrent = State()
    rename_torrent_folder = State()


class AddingTorrent(StatesGroup):
    insert_links = State()
    confirm_adding = State()
