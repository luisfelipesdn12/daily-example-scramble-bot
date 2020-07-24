from telegram.ext import Updater, CommandHandler
from telegram import Bot
import requests, random

API_TOKEN = open("API_TOKEN.txt", "r").read()
keep_going = False

def get_scramble():
    api_uri = "https://scrambler-api.herokuapp.com/3x3x3"
    response = requests.get(api_uri)
    scramble = random.choice(response.json())
    return(scramble)

def scramble(update, context):
    update.message.reply_text(
        f'Hello {update.message.from_user.first_name}, your scramble is {get_scrambles()}'
        )
    print(context.user_data)

def daily_example_scramble():
    message = (
f"""
*Example Solve Diária:*
3x3x3

Embaralhe com o verde na frente e o branco em cima:

{get_scramble()}
"""
    )
    return(message)

bot = Bot(API_TOKEN)
bot.send_message(-1001250429838, text=daily_example_scramble(), parse_mode="Markdown")

if keep_going == True:
    updater = Updater(API_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('scramble', scramble, pass_chat_data=True))

    updater.start_polling()
    updater.idle()