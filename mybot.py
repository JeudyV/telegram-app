import telebot
import requests
import json,urllib.request
import pandas as pd
import ccxt
from pprint import pprint

bot = telebot.TeleBot("768133708:AAGpMhnQFkJmEP5VzR9Cs5MgXXd8ZQy21Jc")

data = urllib.request.urlopen("https://api6.ipify.org/?format=json").read()
output = json.loads(data)

def data_Bitmex():
    bitmex = ccxt.bitmex({}) 
    timeframe = ' '
    since = bitmex.milliseconds () - 500 * 60 * 1000
    candles = bitmex.fetch_ohlcv('BTC/USD', "1m", since, 750)
    return candles

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chatid = message.chat.id
    nombreUser = message.chat.first_name + " " + message.chat.last_name
    greeting = "Hello {nombre}, Welcome to our bot"
    bot.send_message(chatid, greeting.format(nombre=nombreUser))

@bot.message_handler(commands=["help"])
def submitHelp(message):
    chatid = message.chat.id
    mensaje = "functional commands /start, /help, /ip, /csv, /candles_csv"
    bot.send_message(chatid, mensaje)

@bot.message_handler(commands=["ip"])
def submitIp(message):
    chatid = message.chat.id
    pid = output.values()
    bot.send_message(chatid, pid)

@bot.message_handler(commands=["candles_csv"])
def submitcandles(message):
    chatid = message.chat.id
    pCandles = data_Bitmex()
    mensaje = "CSV candles created"
    bot.send_message(chatid, mensaje)
    candles_csv = pd.DataFrame(pCandles)
    candles_csv.to_csv("BTC_metrics.csv")

@bot.message_handler(commands=["csv"])
def createCSV(message):
    chatid = message.chat.id 
    pid = output.values()
    mensaje = "CSV created"
    bot.send_message(chatid, mensaje)
    info = pd.DataFrame(pid)
    info.to_csv("TBOT_file.csv")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chatid = message.chat.id
    bot.send_message(chatid, "functional commands /start, /help, /ip, /csv, /candles_csv")  


bot.polling()