import typing

import qbittorrentapi
from aiogram import types
from aiogram.dispatcher import FSMContext

import states
from .start import bot_start


async def start_adding_torrent(msg: types.Message):
    await msg.answer(
        'Пришлите magnet-ссылку. Чтобы отменить ввод - используйте команду /start',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await states.user.AddingTorrent.insert_links.set()


async def catcher(msg: types.Message, regexp: typing.List[str], qbt: qbittorrentapi.Client, state: FSMContext):
    for i in regexp:
        sent = await msg.answer(f'Добавляется торрент {i}..')
        result = qbt.torrents_add(urls=i)
        await sent.edit_text(sent.text + f'\n{"✅" if "ok" in result.lower() else "❌"}')
    await bot_start(msg, state)
