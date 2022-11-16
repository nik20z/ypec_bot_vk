from loguru import logger
from bot import start_vk_bot

if __name__ == '__main__':

    logger.add("bot/log/info.log",
               format="{time:HH:mm:ss} {level} {module} {function} {message}",
               level="INFO",
               rotation="00:00",
               compression="zip",
               serialize=False,
               enqueue=True)

    with logger.catch():
        start_vk_bot()
