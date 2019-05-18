import telegram
from telegram.ext import *
from telegram import ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import requests
import csv
import os.path
import time
from twython import Twython
from datetime import datetime
import pandas as pd
from dateutil.parser import parse


consumer_key='dO2MDv4LmVZQCkXlTDuvC1Vlf'
consumer_secret='vtdN4SemMWIgGKuHyweXsGBzl4mY5cIa6kYybBIr09ZHhc3qzJ'
access_token_key='1110975440276082688-yNUp3UtVIWVxfYtm68NgEyveXqF1vK'
access_token_secret='TXrNj3cp1AFI5dEYtpnRzMNxV82rr7C2CeuWtRgJXG8Tc'

t_twython = Twython(app_key=consumer_key,
            app_secret=consumer_secret,
            oauth_token=access_token_key,
            oauth_token_secret=access_token_secret)



def get_user_timeline(screen_name, max_id=None, collection=[]):
    global collection_
    try:
        user_timeline = t_twython.get_user_timeline(screen_name=screen_name, count=100, max_id=max_id)
    except Exception as e:
        print(e)
        return collection
    collection_ = collection + user_timeline
    #data = pd.DataFrame(collection)
    #data.to_csv("tweets_date_rank.csv")
    print(
        "Recursively searching... S:{}-E:{}-{}".format(user_timeline[0]["created_at"], user_timeline[-1]["created_at"],
                                                       len(collection_)))
    if max_id == user_timeline[-1]["id"]:
        print("Recursively process has ended... TOTAL ELEMENTS: {}".format(len(collection_)))
        return collection_
    else:
        get_user_timeline(screen_name, max_id=user_timeline[-1]["id"], collection=collection_)
    return collection_


def date_format(date):
    print("date_format entro")
    dt = parse(date)
    print(dt)
    # datetime.datetime(2010, 2, 15, 0, 0)
    valor = dt.strftime('%d/%m/%Y')
    print(valor)
    # 15/02/2010


def get_info(bot, update, args):
    profile = listener(bot, update, args)
    info = get_user_timeline(profile, max_id=None)
    data = pd.DataFrame(info)
    data_top = data.head(160)
    data_top.to_csv("tweets_date_rank.csv")
    print(info)
    send_document_file(bot, update)


def get_date_rank(bot, update, args):
    bandera = False
    profile = listener(bot, update, args)
    info = get_user_timeline(profile, max_id=None)
    date = listener_date(bot, update, args)
    #date = info[12]["created_at"]
    #print(new_date)
    for i in info:
        fecha = date_format(i["created_at"])
        if fecha == date:
            bandera = True
            break
    if bandera == True:
        if not os.path.exists('tweets_date_rank.csv'):
            with open('tweets_date_rank.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Profile", "Tweets"])
                f.close()
        for i in info:
            fecha = date_format(i["created_at"])
            if fecha != date:
                try:
                    with open('tweets_date_rank.csv', 'a', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow([i["created_at"], profile, i["text"]])
                        csvFile.close()
                        print(profile, i["created_at"], i["text"])
                except:
                    print("Unknown error, check your file for possible corrupted or invalid data")
                    bot.sendMessage(chat_id=update.message.chat_id,
                                    text="Unknown error, check your file for possible corrupted"
                                         "or invalid data")
                    pass
            else:
                break
    else:
        print("fecha no existente o fuera del rango de creacion del perfil del usuario")
    #data = pd.DataFrame()
    #data.to_csv("get_date_rank_info.csv")


def send_document_file(bot, update):
    if os.path.exists('tweets_date_rank.csv'):
        bot.sendDocument(chat_id=update.message.chat_id, document=open('tweets_date_rank.csv', 'rb'))


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
    dic = {}
    try:
        twit_box = bs.find_all('li', {'class': 'js-stream-item stream-item stream-item'})
        for box in twit_box:
            txt = box.find('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text
            date_box = box.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})
            date_info = date_box.find('span', {'class': '_timestamp js-short-timestamp'})
            date = date_info.get('data-time')
            array.append(txt)
            array.append(date)
        return array
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


def listener_twit(bot, update, args):
    prof = listener(bot, update, args)
    count_twit = getInfoTwi(prof)
    message = "Tweets for user " + prof + ": " + count_twit + " Tweet"
    bot.sendMessage(chat_id=update.message.chat_id, text=message)
    countMsg = 0
    temp = requests.get('https://twitter.com/' + prof)
    bs = BeautifulSoup(temp.text, 'lxml')
    try:
        twit_box = bs.find_all('li', {'class': 'js-stream-item stream-item stream-item'})
        for box in twit_box:
            txt = box.find('p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'}).text
            date_box = box.find('a', {'class': 'tweet-timestamp js-permalink js-nav js-tooltip'})
            date_info = date_box.find('span', {'class': '_timestamp js-short-timestamp'})
            date = date_info.get('data-time')
            if not os.path.exists('tweets_file.csv'):
                with open('tweets_file.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Profile", "Tweets"])
                    f.close()
            try:
                with open('tweets_file.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(date))), prof, txt])
                    countMsg = countMsg + 1
                    csvFile.close()
            except:
                print("Unknown error, check your file for possible corrupted or invalid data")
                bot.sendMessage(chat_id=update.message.chat_id,
                                text="Unknown error, check your file for possible corrupted"
                                     "or invalid data")
                pass
            if countMsg < 6:
                bot.sendMessage(chat_id=update.message.chat_id, text=txt)
        send_document_file(bot, update)
    except:
        print("Exception in user code:")
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)


def listener(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    if "twitter.com" in profile:
        message2 = profile.split("/")
        for i in range(len(message2)):
            if i + 1 == len(message2):
                profile = message2[i]
    return profile


def listener_date(bot, update, args):
    print("entro")
    #bot.sendMessage(chat_id=update.message.chat_id, text="Reading!")
    profile = str(args[0])
    print(profile)
    message2, date = profile.split("-")
    print(message2)
    print(date)
    return str(date)


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
    add_handler_date = CommandHandler('info', get_info, pass_args=True)
    add_handler_csv = CommandHandler('csv', send_document_file, pass_args=False)


    # Add the handlers to the bot
    dispatcher.add_handler(add_handler_Fllw)
    dispatcher.add_handler(add_handler_Twi)
    dispatcher.add_handler(add_handler_test)
    dispatcher.add_handler(add_handler_date)
    dispatcher.add_handler(add_handler_csv)


    # Starting the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    TOKEN = "768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc"
    main(TOKEN)

while True:
    pass
