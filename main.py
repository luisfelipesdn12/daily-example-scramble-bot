from telegram.ext import Updater, CommandHandler
from telegram import Bot
import requests, random, sys

API_TOKEN = open("API_TOKEN.txt", "r").read()

# > python main.py {keep_going:bool} {alert_groups:bool}

try: keep_going = sys.argv[1].lower() == 'true'
except: keep_going = False

try: alert_groups = sys.argv[2].lower() == 'true'
except: alert_groups = False

groups_subscribed = [-1001250429838, -1001479660521]

def get_n_scrambles(type, n):
    api_uri = f"https://scrambler-api.herokuapp.com/{type}"

    scrambles_list = list()

    while len(scrambles_list) < n:
        five_scrambles = requests.get(api_uri).json()
        scrambles_list += five_scrambles

    while len(scrambles_list) > n:
        scrambles_list.pop()

    return(scrambles_list)

def return_scrambles_formated(cube_type, n):
    error_message = f"Aparently this is not a valid cube type :/ \nOr something went wrong while I've tried to access the data in the API: \nhttps://scrambler-api.herokuapp.com/{cube_type}"

    try: scrambles = get_n_scrambles(cube_type, n)
    except: return(error_message)
    
    if len(scrambles) > 1:
        string_of_formated_scrambles = ""

        for c in range(len(scrambles)):
            string_of_formated_scrambles += f"*{c+1}*. {scrambles[c]}\n\n"

        return(string_of_formated_scrambles)

    else:
        return(scrambles[0])

def scramble(update, context):

    try: cube_type = context.args[0]
    except IndexError: cube_type = "3x3x3"

    try:
        n_of_scrambles = int(context.args[1])
        if n_of_scrambles > 25: n_of_scrambles = 25
    except IndexError: n_of_scrambles = 1

    update.message.reply_text(
        f'Hello {update.message.from_user.first_name}, your {cube_type} scramble is: \n\n{return_scrambles_formated(cube_type, n_of_scrambles)}',
        parse_mode="Markdown"
        )
    print(context.user_data)

def daily_example_scramble(type):
    message = (
f"""
*Example Solve Diária:*
{type}

Embaralhe com o verde na frente e o branco em cima:

{return_scrambles_formated(type, 1)}
"""
    )
    return(message)

bot = Bot(API_TOKEN)

if alert_groups:
    for group_sub in groups_subscribed:
        print(group_sub)
        bot.send_message(group_sub, text=daily_example_scramble("3x3x3"), parse_mode="Markdown")

if keep_going == True:
    updater = Updater(API_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('scramble', scramble, pass_chat_data=True))

    updater.start_polling()
    updater.idle()
