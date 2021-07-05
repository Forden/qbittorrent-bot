from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards.default
import states.user


async def bot_start(msg: types.Message, state: FSMContext):
    await msg.answer(f'Привет, {msg.from_user.full_name}!', reply_markup=keyboards.default.MainMenu.main_menu())
    if await state.get_state() is not None:
        await state.finish()
    await states.user.MainMenu.main_menu.set()
