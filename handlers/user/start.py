from contextlib import suppress

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards.default
import states.user


async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer(f'Главное меню', reply_markup=keyboards.default.MainMenu.main_menu())
    if await state.get_state() is not None:
        with suppress():
            await state.finish()
    await states.user.MainMenu.main_menu.set()
