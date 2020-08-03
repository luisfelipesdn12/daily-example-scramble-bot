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

def get_scramble(type):
    api_uri = f"https://scrambler-api.herokuapp.com/{type}"
    response = requests.get(api_uri)
    scramble = random.choice(response.json())
    return(scramble)

def scramble(update, context):
    scramble = None
    
    try: cube_type = context.args[0]
    except IndexError: cube_type = "3x3x3"

    try: scramble = get_scramble(cube_type)
    except: scramble = f"Aparently this is not a valid cube type :/ \nOr something went wrong while I've tried to access the data in the API: \nhttps://scrambler-api.herokuapp.com/{cube_type}"
    
    update.message.reply_text(
        f'Hello {update.message.from_user.first_name}, your {cube_type} scramble is: \n\n{scramble}'
        )
    print(context.user_data)

def daily_example_scramble(type):
    message = (
f"""
*Example Solve Diária:*
{type}

Embaralhe com o verde na frente e o branco em cima:

{get_scramble(type)}
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
