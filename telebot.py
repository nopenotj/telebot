import config
import logging
import requests
from quiz import initialiseQnBank, next_qn

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)

link = "https://opentdb.com/api.php?amount=10"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
QN, ANS = range(2)
qb = initialiseQnBank(link)
current_qn = next_qn(qb)
points = {}

def start(update, context):
    user = update.message.from_user
    update.message.reply_text("Hello There!")
    nextq(update)
    return QN

def nextq(update):
    reply_keyboard = [[i] for i in current_qn['choices']]
    update.message.reply_text(current_qn['qn'], reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def update_user(user, pt):
    # user = {'id': 53033508, 'first_name': 'jaychua', 'is_bot': False, 'username': 'jamapalJay', 'language_code': 'en'}
    user_id = user['id']
    first_name = user['first_name']
    if user_id in points:
        points[user_id][1] += pt
    else:
        points[user_id] = [first_name,pt]

def print_score():
    string = "Scoreboard\n --------------\n"
    for k,v in points.items():
        string += v[0] + ' : ' + str(v[1]) + '\n'

    return string

def question(update, context):
    user = update.message.text
    global current_qn
    if user == current_qn['ans']:
        current_qn = next_qn(qb)
        update.message.reply_text("Correct!")
        update_user(update.message.from_user, 1)
        update.message.reply_text(print_score())
        nextq(update)
        return QN
    else:
        update.message.reply_text("Wrong!")
        return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Thanks for Playing!!')
    return ConversationHandler.END

def main():

    updater = Updater(config.token, use_context=True)
    #Get dispatcher that registers handlers to deal with updates
    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                QN: [MessageHandler(Filters.text, question)] 
            },
            fallbacks=[CommandHandler('cancel',cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
