# Copyright (C) 2024 ZerProg studios.

import telebot, zerru, time
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot("TOKEN")

def receivingData(data, chat, mess, mode, ERROR=True):
    if mode=="news" or mode=="news_day":
        url = 'https://portal-vr.ru/tag/vr-igry/'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'lxml')

        dataS = soup.find('div', class_="fr-grid-blog").find_all('div', class_="fr-single-news")
        i=0
        text= ""
        images=["","","",""]
        for tt in dataS:
            if i==4:
                break
            images[i]=tt.find("div", class_="b-image").find("a").find("img").get("src")
            text+=f"<b>{tt.find('div', class_='b-content').find('h2').find('a').text}</b>\n"
            text+=tt.find("div", class_="b-content").find("div", class_="fr-single-news__exerpt").find("p").text+"\n\n"
            i+=1
        if ERROR == True:
            bot.delete_message(chat, mess)
        bot.send_photo(chat, images[0])
        bot.send_message(chat, text,parse_mode="html")
    if mode=="games" or mode=="games_day":
        url = r'https://www.hi-fi.ru/magazine/games/top50-vr-games/'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'lxml')

        data = soup.find_all('h3')
        i=49
        text= ""
        while i>=0:
            text+=data[i].text
            text+='\n'
            i-=1
        bot.send_message(chat, text)
        if ERROR == True:
            bot.delete_message(chat, mess)
    if mode=="all":
        url0 = 'https://portal-vr.ru/tag/vr-igry/'

        response0 = requests.get(url0)

        soup0 = BeautifulSoup(response0.content, 'lxml')

        dataS0 = soup0.find('div', class_="fr-grid-blog").find_all('div', class_="fr-single-news")
        i=0
        text= "<b>News: </b>\n"
        images=["","","",""]
        for tt in dataS0:
            if i==3:
                break
            images[i]=tt.find("div", class_="b-image").find("a").find("img").get("src")
            text+=f"<b> {tt.find('div', class_='b-content').find('h2').find('a').text}</b>\n"
            text+=tt.find("div", class_="b-content").find("div", class_="fr-single-news__exerpt").find("p").text+"\n"
            i+=1

        url = r'https://www.hi-fi.ru/magazine/games/top50-vr-games/'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'lxml')

        data = soup.find_all('h3')
        i=49
        text+= "\n<b>Games: </b>\n"
        while i>=0:
            text+=' '
            text+=data[i].text
            text+='\n'
            i-=1
        bot.send_message(chat, text, parse_mode='html')

def receivingDataTime(data, mode1):
    while True:
        time.sleep(1)
        if zerru.DateTime.hour(null=False)==9 and zerru.DateTime.minute(null=False)==0 and zerru.DateTime.second(null=False)==0 or zerru.DateTime.hour(null=False)==18 and zerru.DateTime.minute(null=False)==0 and zerru.DateTime.second(null=False)==0:
            receivingData(data,data.chat.id,data.message_id+1, mode1, False)

@bot.message_handler(commands=["news_day"])
def news_day(data):
    if data.from_user.language_code=="ru":
        bot.send_message(data.chat.id, "Включено")
    else:
        bot.send_message(data.chat.id, "Included")
    receivingDataTime(data,"news_day")
    
@bot.message_handler(commands=["games_day"])
def games_day(data):
    if data.from_user.language_code=="ru":
        bot.send_message(data.chat.id, "Включено")
    else:
        bot.send_message(data.chat.id, "Included")
    receivingDataTime(data,"game_day")

@bot.message_handler(commands=["all_day"])
def all(data):
    if data.from_user.language_code=="ru":
        bot.send_message(data.chat.id, "Включено")
    else:
        bot.send_message(data.chat.id, "Included")
    receivingDataTime(data, "all")  

bot.polling(none_stop=True)
