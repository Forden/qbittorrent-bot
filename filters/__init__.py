from aiogram import Dispatcher

from .is_admin import AdminFilter
from .multiregexp import MultiRegexp


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(MultiRegexp)
