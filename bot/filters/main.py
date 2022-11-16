from vk_maria import types
from vk_maria.dispatcher.filters import AbstractFilter

from bot.config import ADMINS
from bot.database import Select


class NewUserFilter(AbstractFilter):
    """Фильтр на проверку нового пользователя"""
    def check(self, event: types.Message):
        user_id = event.message.from_id
        return Select.user_info_vkontakte(user_id) is None


class AdminFilter(AbstractFilter):
    """Фильтр админов"""
    def check(self, event: types.Message):
        return event.message.from_id in ADMINS


class SyncCodeTextFilter(AbstractFilter):
    """Фильтр для проверки ввода кода синхронизации"""
    def check(self, event: types.Message):
        return event.message.text.strip()[:1] == '#'
