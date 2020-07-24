from telegram.ext import Updater, CommandHandler
import requests, random

API_TOKEN = open("API_TOKEN.txt", "r").read()

def get_scrambles():
    api_uri = "https://scrambler-api.herokuapp.com/3x3x3"
    response = requests.get(api_uri)
    scramble = random.choice(response.json())
    return(scramble)

def scramble(update, context):
    update.message.reply_text(
        f'Hello {update.message.from_user.first_name}, your scramble is {get_scrambles()}'
        )


updater = Updater(API_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('scramble', scramble))

updater.start_polling()
updater.idle()