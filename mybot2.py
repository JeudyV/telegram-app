import telegram
from telegram.ext import *
from bs4 import BeautifulSoup
import requests
import csv
import os.path


def send_document_file(bot, update):
    if os.path.exists('tweets_file.csv'):
        bot.send_document(chat_id=update.message.chat_id, document=open('tweets_file.csv', 'rb'))


def getInfoFllw(profile):
    temp = requests.get('https://twitter.com/' + profile)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        follow_box = bs.find('li', {'class': 'ProfileNav-item ProfileNav-item--followers'})
        followers = follow_box.find('a').find('span', {'class': 'ProfileNav-value'})
        fllw = followers.get('data-count')
        # result = "Followers for user " + profile + ": " + fllw + " users"
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
        # result = "Followers for user " + profile + ": " + fllw + " users"
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
        for box in twit_box:
            txt = box.find('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text
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
    countMsg = 0
    if not os.path.exists('tweets_file.csv'):
        with open('tweets_file.csv', 'a+') as f:
            writer = csv.writer(f)
            writer.writerow(["Profile", "followers"])
            f.close()

    for i in twit_text:
        try:
            with open('tweets_file.csv', 'a', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([prof, i])
                countMsg = countMsg + 1
                csvFile.close()
        except:
            print("Unknown error, check your file for possible corrupted or invalid data")
            bot.sendMessage(chat_id=update.message.chat_id, text="Unknown error, check your file for possible corrupted"
                                                                 "or invalid data")
            pass
        if countMsg < 6:
            bot.sendMessage(chat_id=update.message.chat_id, text=i)
    send_document_file(bot, update)


def listener(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i + 1 == len(message2):
                profile = message2[i]
    return profile


def listener_fllow(bot, update, args):
    prof = listener(bot, update, args)
    result = getInfoFllw(prof)
    chatID = update.message.chat_id
    bot.sendMessage(chat_id=chatID, text=("total amount of followers: ", result))

    with open('followers_file.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(["Profile", "followers"])
        writer.writerow([prof, result])

    csvFile.close()

    """if os.path.exists('followers_file.csv'):
        bot.send_document(chat_id=chatID, document=open('followers_file.csv', 'rb'))
    else:
        print("no existe")"""


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
    # listener_handler = MessageHandler(Filters.text, listenerTwi)
    add_handler_Fllw = CommandHandler('followers', listener_fllow, pass_args=True)
    add_handler_Twi = CommandHandler('tweets', listener_twit, pass_args=True)
    add_handler_test = CommandHandler('test', send_document_file, pass_args=False)

    # Add the handlers to the bot
    dispatcher.add_handler(add_handler_Fllw)
    dispatcher.add_handler(add_handler_Twi)
    dispatcher.add_handler(add_handler_test)

    # Starting the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    TOKEN = "768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc"
    main(TOKEN)

while True:
    pass
