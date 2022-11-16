from psycopg2.errors import ForeignKeyViolation, UndefinedColumn

from bot.database.connect import cursor, connection


def sync_code(user_id: int, user_id_tg_sync_code):
    """Заносим sync_code в настройки пользователя"""
    query = """UPDATE vkontakte 
               SET sync_code = {1} 
               WHERE user_id = {0};
            """.format(user_id, user_id_tg_sync_code)
    try:
        cursor.execute(query)
        return True
    except (ForeignKeyViolation, UndefinedColumn):
        return False


def user_settings_bool(user_id: int, name_: str):
    """Инверсия булевых значений в настройках пользователя"""
    query = """UPDATE vkontakte 
                SET {0} = NOT {0}
                WHERE user_id = {1}
                RETURNING {0}
                """.format(name_, user_id)
    cursor.execute(query)
    connection.commit()
    return cursor.fetchone()[0]
