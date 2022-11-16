from vk_maria.types import KeyboardMarkup, KeyboardModel, Button, Color


class default(KeyboardModel):
    one_time = False
    row1 = [
        Button.Text(Color.PRIMARY, 'Настройки'),
        Button.Text(Color.PRIMARY, 'Расписание')
    ]
    row2 = [
        Button.Text(Color.PRIMARY, 'Рассылка'),
        Button.Text(Color.PRIMARY, 'Помощь')
    ]
