import asyncio
import datetime

import qbittorrentapi
from aiogram import md, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.parts import split_text

import keyboards.default
import states.user
import utils.misc.bytes_helper
from handlers.user import my_torrents
from utils.misc.torrent_state_utils import state_translations


def torrent_data_text(data: qbittorrentapi.TorrentDictionary) -> str:
    m = [
        f'Имя: <b>{md.quote_html(data["name"])}</b>',
        f'Размер: <b>{utils.misc.bytes_helper.byte_to_human_read(data["size"])}</b>',
        f'Прогресс: <b>{round(data["progress"] * 100, 2)}%</b>',
        f'Статус: <b>{state_translations[data["state"]]}</b>',
        f'Сиды: <b>{data["num_seeds"]}</b> ({data["num_complete"]})',
        f'Пиры: <b>{data["num_leechs"]}</b> ({data["num_incomplete"]})',
        f'Загрузка: <b>{utils.misc.bytes_helper.byte_to_human_read(data["dlspeed"])}/с</b>',
        f'Отдача: <b>{utils.misc.bytes_helper.byte_to_human_read(data["upspeed"])}/с</b>',
        'eta',
        f'Рейтинг: {round(data["ratio"], 2)}' + ('✅' if data['ratio'] >= 1 else '❌'),
        f'Категория: {data["category"]}' if data['category'] else None,
        f'Метки: {", ".join(data["tags"].split(","))}' if data['tags'] else None,
        f'Дата добавления: {datetime.datetime.fromtimestamp(data["added_on"])}',
    ]
    if data['amount_left'] and not data.state_enum.is_paused:
        if data['eta'] < 8640000:
            m[m.index('eta')] = f'Осталось времени: <b>{datetime.timedelta(seconds=data["eta"])}</b>'
        else:
            m[m.index('eta')] = '∞'
    else:
        m[m.index('eta')] = None
    m = filter(lambda k: bool(k), m)
    return '\n'.join(m)


async def get_torrent_data(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    torrents: qbittorrentapi.TorrentDictionary = qbt.torrents.info()
    torrents_names = list(map(lambda k: k['name'], torrents))
    if msg.text in torrents_names:
        target_torrent = torrents[torrents_names.index(msg.text)]
        update_msg = await msg.answer(
            torrent_data_text(target_torrent),
            reply_markup=keyboards.default.MainMenu.torrent_data(target_torrent)
        )
        await states.user.MainMenu.inspecting_torrent.set()
        await state.update_data(hash=target_torrent['hash'])
        await state.update_data(last_update_message_id=update_msg.message_id)
    else:
        await my_torrents(msg, qbt)


async def update_torrent_data(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            data = torrents[0]
            last_update_message = await msg.answer(
                torrent_data_text(data), reply_markup=keyboards.default.MainMenu.torrent_data(data)
            )
            await msg.delete()
            await msg.bot.delete_message(chat_id=msg.chat.id, message_id=storage['last_update_message_id'])
            last_update_message_id = last_update_message.message_id
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    await state.update_data(last_update_message_id=last_update_message_id)


async def pause_torrent(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    paused = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_pause(torrent_hashes=storage['hash'])
            paused = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    if paused:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.2)
        await update_torrent_data(msg, qbt, state)


async def resume_torrent(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    resumed = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_resume(torrent_hashes=storage['hash'])
            resumed = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    if resumed:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.5)
        await update_torrent_data(msg, qbt, state)


async def force_start_torrent(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    started = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_set_force_start(torrent_hashes=storage['hash'], enable=True)
            started = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    if started:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.2)
        await update_torrent_data(msg, qbt, state)


async def recheck_torrent(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    rechecked = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_recheck(torrent_hashes=storage['hash'])
            rechecked = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    if rechecked:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.2)
        await update_torrent_data(msg, qbt, state)


async def reannounce_torrent(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    reannounced = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_reannounce(torrent_hashes=storage['hash'])
            reannounced = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    if reannounced:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.2)
        await update_torrent_data(msg, qbt, state)


async def get_magnet_url(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            parts = list(map(md.quote_html, split_text(torrents[0]["magnet_uri"], 4000)))
            for i in parts:
                await msg.answer(f'<code>{i}</code>')
                await asyncio.sleep(.1)
            if len(parts) > 1:
                await msg.answer('Magnet-ссылка слишком длинная, отправлена по частям.')
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')


async def start_renaming_torrent(msg: types.Message):
    await msg.answer(
        'Введите новое имя торрента. Чтобы отменить ввод - используйте команду /start',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await states.user.MainMenu.rename_torrent.set()


async def set_torrent_name(msg: types.Message, qbt: qbittorrentapi.Client, state: FSMContext):
    await msg.chat.delete_message(msg.message_id - 1)
    renamed = False
    async with state.proxy() as storage:
        torrents = qbt.torrents.info(torrent_hashes=storage['hash'])
        if torrents:
            qbt.torrents_rename(torrent_hash=storage['hash'], new_torrent_name=msg.text)
            renamed = True
        else:
            await msg.answer('Торрент был удален. Используйте команду /start')
    await states.user.MainMenu.inspecting_torrent.set()
    if renamed:
        await msg.answer_chat_action('typing')
        await asyncio.sleep(.2)
        await update_torrent_data(msg, qbt, state)
