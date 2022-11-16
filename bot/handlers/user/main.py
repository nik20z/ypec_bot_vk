from datetime import datetime
from loguru import logger

from vk_maria.dispatcher import Dispatcher
from vk_maria.types import Message

# My Modules
from bot.config import AnswerText

from bot.database import Insert
from bot.database import Select
from bot.database import Update

from bot.filters import NewUserFilter
from bot.filters import SyncCodeTextFilter

from bot.functions import get_user_id
from bot.functions import get_sync_code
from bot.functions import create_name_list_text
from bot.functions import get_condition_smile

from bot.message_timetable import MessageTimetable

from bot.keyboards import Reply


# vk.messages_send(user_id=event.message.from_id, message='Добро пожаловать!')


def new_user(event: Message):
    """Обработчик для нового пользователя"""
    user_id = event.message.from_id
    joined = datetime.utcfromtimestamp(event.message.date)
    user_name = ""

    if user_id > 0:
        text = AnswerText.new_user["welcome_message_private"](user_name)
    else:
        text = AnswerText.new_user["welcome_message_group"](user_name)

    new_user_data = (user_id, user_name, joined)
    Insert.new_user(new_user_data)

    event.answer(text)
    logger.info(f"message {user_id}")


def check_sync_code(event: Message):
    """Пользователь ввёл код синхронизации"""
    user_id = event.message.from_id
    sync_code = event.message.text.strip().upper()
    user_id_tg_sync_code = get_user_id(sync_code)

    keyboard = Reply.default

    if Update.sync_code(user_id, user_id_tg_sync_code):
        text = AnswerText.set_sync_code
    else:
        text = AnswerText.error_set_sync_code

    event.answer(text, keyboard=keyboard)


def update_spamming(event: Message):
    """Обновить значение параметра Рассылка"""
    user_id = event.message.from_id
    result = Update.user_settings_bool(user_id, 'spamming')

    text = AnswerText.update_spamming(result)
    keyboard = Reply.default
    event.answer(text, keyboard=keyboard)
    logger.info(f"message {user_id}")


def sync_code_empty(event: Message):
    """Если отсутствует код синхронизации"""
    user_id = event.message.from_id
    text = AnswerText.sync_code_empty
    keyboard = Reply.default
    event.answer(text, keyboard=keyboard)
    logger.info(f"message {user_id}")


def timetable(event: Message):
    """Обработчик запроса на получение Расписания"""
    user_id = event.message.from_id
    user_id_tg_sync_code = Select.get_sync_code(user_id)

    keyboard = Reply.default

    if user_id_tg_sync_code is None:
        """Если отсутствует код синхронизации"""
        return sync_code_empty(event)

    user_info = Select.user_info_by_column_names(user_id_tg_sync_code)

    type_name = user_info[0]
    name_id = user_info[1]
    view_name = user_info[2]
    view_add = user_info[3]
    view_time = user_info[4]

    if type_name is None or name_id is None:
        """У пользователя нет основной подписки"""
        logger.info(f"message no_main_subscription {user_id}")
        return event.answer(AnswerText.no_main_subscription, keyboard=keyboard)

    name_ = Select.name_by_id(type_name, name_id)

    date_ = Select.fresh_ready_timetable_date(type_name=type_name, name_id=name_id)

    data_ready_timetable = Select.ready_timetable(type_name, date_, name_)

    text = MessageTimetable(name_,
                            date_,
                            data_ready_timetable,
                            view_name=view_name,
                            view_add=view_add,
                            view_time=view_time).get()

    event.answer(text, keyboard=keyboard)
    logger.info(f"message {user_id}")


def settings(event: Message):
    """Обработчик запроса на получение Настроек пользователя"""
    user_id = event.message.from_id
    user_settings_vkontakte = Select.user_info_vkontakte(user_id)
    user_id_sync_code = user_settings_vkontakte[2]
    spamming_vk = user_settings_vkontakte[3]

    if user_id_sync_code is None:
        """Если отсутствует код синхронизации"""
        return sync_code_empty(event)

    user_settings_data = list(Select.user_info_telegram(user_id_sync_code))
    table_name = user_settings_data[0]
    name_ = user_settings_data[1]
    name_id = user_settings_data[2]
    groups_array = user_settings_data[3]
    teachers_array = user_settings_data[4]

    spamming = user_settings_data[5]
    pin_msg = user_settings_data[6]
    view_name = user_settings_data[7]
    view_add = user_settings_data[8]
    view_time = user_settings_data[9]

    if name_id is not None:
        name_ = Select.name_by_id(table_name, name_id)

    text = f"{get_sync_code(user_id_sync_code)}\n"
    main_subscribe_text = '--отсутствует--' if name_id is None else f"⭐ {name_}"
    text += f"Главная подписка:\n {main_subscribe_text}\n"

    if groups_array:
        text += '\n'
        text += create_name_list_text('group_', groups_array)

    if teachers_array:
        text += '\n'
        text += create_name_list_text('teacher', teachers_array)

    text += f"\nРассылка вк: {'✅' if spamming_vk else '☑'}\n\n"
    text += "\nОсновные настройки:\n"

    p = '&#8196;'
    # 8196
    # 8197
    # 8198
    # 8202
    text += f"Рассылка{p*3}&#8202;{get_condition_smile(spamming)}\n"
    text += f"Закреплять {get_condition_smile(pin_msg)}\n"
    text += f"Заголовок{p*2}&#8202;{get_condition_smile(view_name)}\n"
    text += f"Подробно{p*3}{get_condition_smile(view_add)}\n"
    text += f"Время{p*8}{get_condition_smile(view_time)}\n"

    keyboard = Reply.default
    event.answer(text, keyboard=keyboard)
    logger.info(f"message {user_id}")


def help_message(event: Message):
    """Вывести help-сообщение"""
    user_id = event.message.from_id
    event.answer(AnswerText.help)
    logger.info(f"message {user_id}")


def other_messages(event: Message):
    """Обработчик сторонних сообщений"""
    user_id = event.message.from_id
    text = AnswerText.other_messages
    keyboard = Reply.default
    event.answer(text, keyboard=keyboard)
    logger.info(f"message {user_id}")


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers

    dp.register_message_handler(new_user, NewUserFilter)

    dp.register_message_handler(check_sync_code, SyncCodeTextFilter)

    dp.register_message_handler(update_spamming, commands=['Рассылка', 'spamming'])

    dp.register_message_handler(timetable, commands=['Расписание', 'timetable'])

    dp.register_message_handler(settings, commands=['Настройки', 'settings'])

    dp.register_message_handler(help_message, commands=['Помощь', 'help'])

    dp.register_message_handler(other_messages)
