#!/usr/bin/env python

"""Main for bot."""

# ----------------------------------------------
# Copyright: Daniel Bebber, 2020
# Author: Daniel Bebber <daniel.bebber@gmx.de>
# ----------------------------------------------
import json
import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
from control.database_controller import DatabaseController
from utils.path_utils import DATA_PATH

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

db_controller = DatabaseController()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    user = update.message.from_user
    update.message.reply_text('Ich leg erstmal eine neue Datenbank für dich an {} ..'.format(user.first_name))
    db_controller.load_event_data(user.id)
    created = db_controller.check_or_create_database(user.id)
    if not created:
        update.message.reply_text('Oh! Anscheinend warst du schon mal hier - na dann nehmen wir doch was schon da ist.')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text("Eigentlich soll ich was besseres tun. Vielleicht irgendwann ja mal...")


def main():
    """Start the bot."""

    token_file_path = os.path.join(DATA_PATH, ".token")
    if not token_file_path:
        raise RuntimeError("Token file {} was not found!".format(token_file_path))

    with open(token_file_path) as token_file:
        token = token_file.read()

    if not token:
        raise RuntimeError("Token in {} was empty".format(token_file_path))

    # Create the Updater and pass it your bots token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
