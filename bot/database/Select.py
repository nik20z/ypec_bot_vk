from bot.database.connect import cursor


def check_none(func):
    """Обработчик None-значений"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return None if not result else result[0]

    return wrapper


def user_info_vkontakte(user_id: int):
    """Получить данные о пользователе"""
    query = """SELECT user_id, 
                      user_name, 
                      sync_code,
                      spamming
                FROM vkontakte
                WHERE user_id = {0}
                """.format(user_id)
    cursor.execute(query)
    return cursor.fetchone()


def user_info_telegram(user_id: int):
    """Получить данные о пользователе"""
    query = """SELECT  CASE WHEN type_name THEN 'group_' ELSE 'teacher' END,
                        '',
                        name_id,
                        ARRAY(SELECT ARRAY[group__id::text, group__name, (group__id = ANY(spam_group__ids))::text]
                              FROM group_
                              WHERE ((type_name ISNULL) OR NOT(group__id = name_id AND type_name)) AND group__id = ANY(group__ids)) AS group__ids,
                        ARRAY(SELECT ARRAY[teacher_id::text, teacher_name, (teacher_id = ANY(spam_teacher_ids))::text]
                              FROM teacher
                              WHERE ((type_name ISNULL) OR NOT(teacher_id = name_id AND NOT type_name)) AND teacher_id = ANY(teacher_ids)) AS teacher_ids,
                        spamming, 
                        pin_msg, 
                        view_name, 
                        view_add, 
                        view_time
                FROM telegram
                WHERE user_id = {0}
                """.format(user_id)
    cursor.execute(query)
    return cursor.fetchone()


def get_sync_code(user_id: int):
    """Проверка на наличие sync_code у пользователя"""
    query = """SELECT sync_code
                FROM vkontakte 
                WHERE user_id = {0};
                """.format(user_id)
    cursor.execute(query)
    return cursor.fetchone()[0]


def user_info_by_column_names(user_id: int, column_names=None, table_name="telegram"):
    """Данные о пользователе по конкретным колонкам"""
    if column_names is None:
        column_names = ["CASE WHEN type_name THEN 'group_' WHEN not type_name THEN 'teacher' ELSE NULL END",
                        "name_id",
                        "view_name",
                        "view_add",
                        "view_time"]
    query = """SELECT {1}
                    FROM {2}
                    WHERE user_id = {0}
                    """.format(user_id,
                               ', '.join(column_names),
                               table_name)
    cursor.execute(query)
    return cursor.fetchone()


@check_none
def name_by_id(type_name: str, name_id: str):
    """Получить name_ группы или преподавателя по id"""
    query = "SELECT {0}_name FROM {0} WHERE {0}_id = {1}".format(type_name, name_id)
    cursor.execute(query)
    return cursor.fetchone()


@check_none
def fresh_ready_timetable_date(type_name=None, name_id=None):
    """Получить дату актуального расписания по типу профиля и id"""
    where_add = "True"
    if type_name is not None and name_id is not None:
        where_add = f"{type_name}_id = {name_id}"

    query = """SELECT to_char(date_, 'DD.MM.YYYY')
                   FROM ready_timetable
                   WHERE {0}
                   ORDER BY date_ DESC
                   LIMIT 1
                   """.format(where_add)
    cursor.execute(query)
    return cursor.fetchone()


def ready_timetable(type_name: str, date_: str, name_: str):
    """Получить готовое расписание"""
    reverse_type_name = {'group_': 'teacher', 'teacher': 'group_'}.get(type_name)
    query = """
                SELECT array_agg(DISTINCT num_lesson) AS num_les,
                       array_agg(DISTINCT COALESCE(NULLIF(lesson_name, ''), '...')),
                       json_object_agg(DISTINCT COALESCE(NULLIF({0}_name, ''), '...'), audience_name),
                       ARRAY[NULL]
                FROM ready_timetable_info
                WHERE date_ = '{2}' AND {1}_name = '{3}'
                GROUP BY lesson_name, {0}_name, audience_name
                ORDER BY num_les
                """.format(reverse_type_name,
                           type_name,
                           date_,
                           name_)
    cursor.execute(query)
    return cursor.fetchall()
