import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from bs4 import BeautifulSoup
import requests


def getinfoDate(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        data_box = bs.find('small', {'class': 'time'})
        dataTwit = data_box.find('a').find('span', {'class': '_timestamp js-short-timestamp'})
        data = dataTwit.get('data-time')
        result = "Data for tweet " + profile + ": " + data + " users"
        return result
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


"""def getBoxTwit(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        twit_box = bs.find_all('ol', {'class': 'stream-items js-navigable-stream'}, limit=5)
        for box in twit_box:
            Box_id = box.find('li', {'class': 'js-stream-item stream-item stream-item js-pinned'})
            id = Box_id.get('data-item-id')
            print(id)
            #print(box.get('data-item-id'))
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)"""


def getTextTwit(profile):
    array = []
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        twit_box = bs.find_all('li', {'class': 'js-stream-item stream-item stream-item'})
        for box in range(len(twit_box)-15):
            txt = twit_box[box].find('p', {'class': 'TweetTextSize TweetTextSize--normal '
                                                    'js-tweet-text tweet-text'}).text
            print("txt", txt)
            array.append(txt)
        return array
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


def listener(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    print("param", profile)
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    return profile


def listenerBox(bot, update, args):
    prof = listener(bot, update, args)
    result = getTextTwit(prof)
    for x in result:
        bot.sendMessage(chat_id=update.message.chat_id, text=x)


def listenerData2(bot, update, args):
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
    result = getBoxTwit(profile)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)


def listenerData(bot, update, args):
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
    result = getInfoDate(profile)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)


def start(bot, update):
  """ This function will be executed when '/start' command is received """
  message = "Welcome to the coolest bot ever!"
  bot.send_message(chat_id=update.message.chat_id, text=message)


def hello(bot, update):
  """ This function will be executed when '/hello' command is received """
  greeting = "Hi there, {}".format(update.effective_user.username)
  bot.send_message(chat_id=update.message.chat_id, text=greeting)


def add(bot, update, args):
  """ This function will be executed when '/add arg1, arg2, ...' command is received """

  # First converts the string list to a int list and then add all the elems
  result = sum(map(int, args))
  message = "The result is: {}".format(result)
  bot.send_message(chat_id=update.message.chat_id, text=message)


def main(bot_token):
    """ Main function of the bot """
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    start_handler = CommandHandler('start', start)
    hello_handler = CommandHandler('hello', hello)
    add_handler = CommandHandler('add', add, pass_args=True)
    add_handler_box = CommandHandler('box', listenerBox, pass_args=True)

    # Add the handlers to the bot
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(hello_handler)
    dispatcher.add_handler(add_handler)
    dispatcher.add_handler(add_handler_box)

    # Starting the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    TOKEN = "768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc"
    main(TOKEN)


