from bot.functions import get_condition_smile


GOD_ID = 311084510
ADMINS = [311084510, 264311526]


class AnswerText:
    new_user = {
        "welcome_message_private": lambda
            user_name: f"Привет {user_name} (^_^)\n"
                       f"Я бот колледжа ЯПЭК, созданный для связки с главным телеграм-ботом\n"
                       f"Для подключения своего аккаунта просто введи код синхронизации\n",
        "welcome_message_group": lambda
            user_name: f"Приветствую всех в группе {user_name} (^_^)\n"
                       f"Я бот колледжа ЯПЭК, созданный для связки с главным телеграм-ботом\n"
                       f"Для подключения своего аккаунта просто введи код синхронизации\n",
    }
    no_main_subscription = "Вы не оформили основную подписку В Телеграм!\nСделайте это в меню /settings или с помощью команды /start"
    sync_code_empty = "Вы ещё не прислали код синхронизации"
    set_sync_code = "Отлично, код принят)"
    error_set_sync_code = "Такого кода не существует!"
    update_spamming = lambda result: f"Рассылка {'активирована' if result else 'удалена'} {get_condition_smile(result)}"

    help = "Описание команд\n" \
           "Расписание - вывести расписание\n" \
           "Настройки - получить настройки, согласно коду синхронизации\n" \
           "Рассылка - меняем параметр Рассылка для вк\n" \
           "\n" \
           "Чтобы обновить код синхронизации, просто пришлите боту новый\n" \
           ""
    other_messages = 'На данный момент я реагирую только на команды клавиатуры ⬇'


CALL_SCHEDULE = {"weekday": {
    '0': ('7:40', '8:25'),
    '1': ('8:30', '10:00'),
    '2': ('10:20', '11:50'),
    '3': ('12:20', '13:50'),
    '4': ('14:05', '15:35'),
    '5': ('15:55', '17:25'),
    '6': ('17:35', '19:05'),
    '7': ('19:10', '20:40')
},
    "saturday": {
        '1': ('8:30', '10:00'),
        '2': ('10:10', '11:40'),
        '3': ('11:55', '13:25'),
        '4': ('13:35', '15:05')
    }
}
