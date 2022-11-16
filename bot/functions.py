from datetime import datetime


def get_sync_code(user_id: int):
    """Получаем sync_code из user_id"""
    sync_code = "#"
    if user_id > 0:
        sync_code += 'U'
    else:
        sync_code += 'G'
        user_id *= -1
    for i in str(user_id):
        sync_code += chr(int(i) + 65)
    return sync_code


def get_user_id(sync_code: str):
    """Получаем user_id из sync_code"""
    user_id = ""
    for i in sync_code[2:]:
        user_id += str(ord(i) - 65)
    if user_id.isdigit():
        # если код пользователя
        if sync_code[1] == 'U':
            return int(user_id)
        return -1 * int(user_id)


def get_week_day_id_by_date_(date_: str, format_str="%d.%m.%Y"):
    """Получить номер недели по дате"""
    return datetime.strptime(date_, format_str).weekday()


def create_name_list_text(type_name: str, names_array: list):
    """Создаём список подписок"""
    text = "Группы:\n" if type_name == 'group_' else 'Преподаватели:\n'
    for one_name in names_array:
        name_ = one_name[1]
        spam_state = one_name[2]
        smile_spam_state = '🌀' if spam_state == 'true' else ''
        text += f"{name_} {smile_spam_state}\n"
    return text


def get_condition_smile(bool_value: bool):
    return '✅' if bool_value else '☑'
