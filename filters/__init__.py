from aiogram import Dispatcher
from filters.is_admin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)