#!/usr/bin/env python3
from secrets.secret import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import logging
import time
import sys

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger()
updater = Updater(token=TOKEN, use_context=True)

if len(sys.argv) != 2:
    print('Usage: %s [username]' % sys.argv[0])
    exit(1)

notification_chat_id = None
notification_username = sys.argv[1]

# Handlers
handlers = dict()

handlers['start'] = 'start_handler'
def start_handler(update, context):
    if update.effective_chat.username == notification_username:
        logger.info('NICE!!, Your chat_id: %d' % (update.effective_chat.id))
        global notification_chat_id
        notification_chat_id = update.effective_chat.id
    logger.info('Got message from (username = %s, id = %d)' % (update.effective_chat.username, update.effective_chat.id))
    context.bot.send_message(update.effective_chat.id, text="I can send notifications to %s. Use /ping to send notification." % (notification_username))

handlers['ping'] = 'ping_handler'
def ping_handler(update: Update, context: CallbackContext):
    curr_chat = update.effective_chat
    if notification_chat_id is None:
        context.bot.send_message(curr_chat.id, 'Can\' get user chat id. Call @%s and say to write me' % (notification_username))
    else:
        context.bot.send_message(notification_chat_id, 'Ping from %s (%s %s)' % (curr_chat.username, curr_chat.first_name, curr_chat.last_name))
        context.bot.send_message(curr_chat.id, '%s has been notified' % (notification_username))


dispatcher = updater.dispatcher
for command, handler in handlers.items():
    dispatcher.add_handler(CommandHandler(command, eval(handler)))

# Handlers


updater.start_polling()
