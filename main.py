# -*- coding: utf-8 -*-
import logging

from utils.set_bot_commands import set_default_commands
from handlers.default_handlers import *
from database.models import models_main
from loader import *

# Logging settings
logging.basicConfig(
    level=logging.INFO,  # Уровень - INFO
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
    filename="bot.log",  # File for logging
)


def main():
    logging.info("Creating database...")
    models_main()
    logging.info("...")
    logging.info("Database created...")

    set_default_commands(bot)

    logging.info("Starting Telegram bot...")
    bot.infinity_polling()
    logging.info("Telegram bot started...")


main()
