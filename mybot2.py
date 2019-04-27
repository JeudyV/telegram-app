import telegram
from telegram.ext import *
from bs4 import BeautifulSoup
import requests

#mi_bot = telegram.Bot("768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc")
#mi_bot_updater = Updater(mi_bot.token)


def getInfoFllw(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        follow_box = bs.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'})
        followers = follow_box.find('a').find('span', {'class': 'ProfileNav-value'})
        fllw = followers.get('data-count')
        result = "Followers for user " + profile + ": " + fllw + " users"
        return result
    except:
        print("Exception in user code:")
        print('-' * 60) 
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

def getInfoTwi(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        follow_box = bs.find('li', {'class': 'ProfileNav-item ProfileNav-item--tweets is-active'})
        followers = follow_box.find('a').find('span', {'class': 'ProfileNav-value'})
        fllw = followers.get('data-count')
        result = "Followers for user " + profile + ": " + fllw + " users"
        return result
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

def listenerFllw(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    #profile = str(update.message.text)
    profile = str(args[0])
    print("param", profile)
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    print(profile)
    result = getInfoFllw(profile)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)

def listenerTwi(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    #profile = str(update.message.text)
    profile = str(args[0])
    print("param", profile)
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    print(profile)
    result = getInfoTwi(profile)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)

#listener_handler = MessageHandler(Filters.text, listener)
#variable = CommandHandler("tweets", listenerTwi)
#mi_bot_updater.dispatcher.add_handler(listener_handler)

#mi_bot_updater.start_polling()
#mi_bot_updater.idle()

def main(bot_token):
  """ Main function of the bot """
  updater = Updater(token=bot_token)
  dispatcher = updater.dispatcher

  # Other handlers
  #listener_handler = MessageHandler(Filters.text, listenerTwi)
  add_handler_Fllw = CommandHandler('followers', listenerFllw, pass_args=True)
  add_handler_Twi = CommandHandler('tweets', listenerTwi, pass_args=True)

  # Add the handlers to the bot
  #dispatcher.add_handler(listener_handler)
  dispatcher.add_handler(add_handler_Fllw)
  dispatcher.add_handler(add_handler_Twi)


  # Starting the bot
  updater.start_polling()
  updater.idle()

if __name__ == "__main__":
  TOKEN = "768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc"
  main(TOKEN)

while True:
    pass

