import telegram
from telegram.ext import *
from bs4 import BeautifulSoup
import requests
import csv


def getInfoFllw(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        follow_box = bs.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'})
        followers = follow_box.find('a').find('span', {'class': 'ProfileNav-value'})
        fllw = followers.get('data-count')
        #result = "Followers for user " + profile + ": " + fllw + " users"
        return fllw
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
        Twit = followers.get('data-count')
        #result = "Followers for user " + profile + ": " + fllw + " users"
        return Twit
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


def getTextTwit(profile):
    array = []
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        twit_box = bs.find_all('li', {'class': 'js-stream-item stream-item stream-item'})
        for box in range(len(twit_box)-15):
            txt = twit_box[box].find('p', {'class': 'TweetTextSize TweetTextSize--normal '
                                                    'js-tweet-text tweet-text'}).text
            array.append(txt)
        return array
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


def listener_twit(bot, update, args):
    prof = listener(bot, update, args)
    twit_text = getTextTwit(prof)
    count_twit = getInfoTwi(prof)
    message = "Tweets for user " + prof + ": " + count_twit + " Tweet"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    for x in twit_text:
        bot.sendMessage(chat_id=update.message.chat_id, text=x)


def listener(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    return profile


def listener_fllow(bot, update, args):
    prof = listener(bot, update, args)
    result = getInfoFllw(prof)
    bot.sendMessage(chat_id=update.message.chat_id, text=("total amount of followers: ",result))
    twit_file = csv.writer(open("followers_file.csv", "w"))
    twit_file.writerow(["Profile", "followers"])
    twit_file.writerow([prof, result])


def listenerT(bot, update, args):
    prof = listener(bot, update, args)
    result = getInfoTwi(prof)
    bot.sendMessage(chat_id=update.message.chat_id, text=("total amount of tweets: ", result))
    twit_file = csv.writer(open("tweets_file.csv", "w"))
    twit_file.writerow(["Profile", "tweets"])
    twit_file.writerow([prof, result])


"""def listenerFllw(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    print("param", profile)
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    print(profile)
    result = getInfoFllw(profile)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)"""


"""def listenerTwi(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    print("param", profile)
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i+1 == len(message2):
                profile = message2[i]
    print(profile)
    result = str(getInfoTwi(profile))
    print(result)
    bot.sendMessage(chat_id=update.message.chat_id, text=result)
    twit_file = csv.writer(open("tweets_file.csv", "w"))
    twit_file.writerow(["Profile", "tweets"])
    twit_file.writerow([profile, result])"""


def main(bot_token):
    """ Main function of the bot """
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Other handlers
    #listener_handler = MessageHandler(Filters.text, listenerTwi)
    add_handler_Fllw = CommandHandler('followers', listener_fllow, pass_args=True)
    add_handler_Twi = CommandHandler('tweets', listener_twit, pass_args=True)

    # Add the handlers to the bot
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

