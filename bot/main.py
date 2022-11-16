from vk_maria import Vk
from vk_maria.dispatcher import Dispatcher

from vk_maria.dispatcher.fsm import MemoryStorage
#from vk_maria.dispatcher.fsm import StatesGroup, State, MemoryStorage, FSMContext

from bot.handlers import register_all_handlers
from bot.misc import Keys
from bot.database import Table


def on_startup(dp: Dispatcher):
    register_all_handlers(dp)


def on_shutdown(dp: Dispatcher):
    dp._storage.close()
    #dp.storage.wait_closed()
    pass


def start_vk_bot():
    Table.create()

    vk = Vk(access_token=Keys.VK_TOKEN)
    dp = Dispatcher(vk, MemoryStorage())

    dp.start_polling(debug=True,
                     on_startup=on_startup(dp),
                     on_shutdown=on_shutdown(dp))
