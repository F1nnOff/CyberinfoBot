import telebot
import requests
from bs4 import BeautifulSoup
import datetime
import sys

bot = telebot.TeleBot("1945741488:AAGusRDHDoIurQcQ5RXtsP2t-qU5hdm-b2Q")
commands = ["/help", "/start", "/day", "/team", "/stats", "/results", "/teamstat", "/playerstat"]


@bot.message_handler(commands=['start'])
def startbot(message):
    bot.send_message(message.chat.id, "Приветсвую Вас в telegram bot'е CyberInfo! Вы можете следить за любимыми "
                                      "командами по дисциплине CS:GO, что позволит не пропустить ни одного "
                                      "интересного матча. Для выбора команд напишите /help")


@bot.message_handler(commands=['help'])
def helpbot(message):
    bot.send_message(message.chat.id, "команда начала /start")
    bot.send_message(message.chat.id, "время матчей в определенный день /day")
    bot.send_message(message.chat.id, "время всех ближайших матчей определенной команды /team")
    bot.send_message(message.chat.id, "узнать статистику игроков и команд /stats")
    bot.send_message(message.chat.id, "результаты матчей за последние 7 дней /results")


@bot.message_handler(commands=['day'])
def day(message):
    bot.send_message(message.chat.id, 'Выберете дату, по которой хотите увидеть матчи в формате "yyyy-mm-dd"')
    bot.register_next_step_handler(message, daysearch)


@bot.message_handler(commands=['team'])
def team(request):
    bot.send_message(request.chat.id, 'Выберете команду(официальное название), ближайшие матчи которой хотите увидеть')
    bot.register_next_step_handler(request, teamsearch)


@bot.message_handler(commands=['stats'])
def stat(message):
    bot.send_message(message.chat.id, 'Статистика по лучшим командам /teamstat')
    bot.send_message(message.chat.id, 'Статистика по лучшим игрокам /playerstat')


@bot.message_handler(commands=['teamstat'])
def tstat(message):
    # Парсим -----------------------
    url = 'https://www.hltv.org/stats'
    htmlcode = requests.get(url).text
    soup = BeautifulSoup(htmlcode, "lxml")
    teamclass = "col"
    days = soup.find_all("div", class_=teamclass)
    bot.send_message(message.chat.id, '\n'.join(days[1].text.split("\n\n\n")))


@bot.message_handler(commands=['playerstat'])
def pstat(message):
    # Парсим -----------------------
    url = 'https://www.hltv.org/stats'
    htmlcode = requests.get(url).text
    soup = BeautifulSoup(htmlcode, "lxml")
    teamclass = "col"
    days = soup.find_all("div", class_=teamclass)
    bot.send_message(message.chat.id, '\n'.join(days[0].text.split("\n\n\n")))


@bot.message_handler(commands=['results'])
def result(request):
    bot.send_message(request.chat.id, 'Выберете дату, по которой хотите увидеть рузультаты матчей в формате '
                                      '"July 18th"')
    bot.register_next_step_handler(request, resultsearch)


@bot.message_handler(content_types=['text'])
def trash(request):
    if requests not in commands:
        bot.send_message(request.chat.id, 'Введите верную команду из предложенных в /help')


def daysearch(request):
    # bot.send_message(message.chat.id, type(message))
    if len(request.text) != 10:
        bot.send_message(request.chat.id, 'Дата введена некоректно, мы хотим увидеть ее в формате "yyyy-mm-dd"')
        return
    else:
        for i in range(len(request.text)):
            if i != 4 and i != 7:
                if request.text[i].isalpha():
                    bot.send_message(request.chat.id,
                                     'Дата введена некоректно, мы хотим увидеть ее в формате "yyyy-mm-dd"')
                    return
            else:
                if request.text[i] != '-':
                    bot.send_message(request.chat.id,
                                     'Дата введена некоректно, мы хотим увидеть ее в формате "yyyy-mm-dd"')
                    return
        now = datetime.datetime.now()
        if str(now)[:10] > request.text:
            bot.send_message(request.chat.id,
                             'Дата введена некоректно, эта дата уже в прошлом, вы можете посмотреть результаты '
                             'сыгранных матчей /results') 
            return
    # Парсим -----------------------
    url = 'https://www.hltv.org/matches'
    htmlcode = requests.get(url).text
    soup = BeautifulSoup(htmlcode, "lxml")
    dayclass = "upcomingMatchesSection"
    days = soup.find_all("div", class_=dayclass)
    for item in days:
        if item.text.find(request.text, 0, len(item.text)) != -1:
            # bot.send_message(message.chat.id, item.text)
            bot.send_message(request.chat.id, '\t\t\t\t\t'.join(item.text.split("\n\n\n\n")))
            return
    # ------------------------------
    bot.send_message(request.chat.id, "В выбранную вами дату на данный момент матчей нет")
    return


def teamsearch(request):
    # Парсим -----------------------
    url = 'https://www.hltv.org/matches'
    htmlcode = requests.get(url).text
    soup = BeautifulSoup(htmlcode, "lxml")
    dayclass = "upcomingMatchesSection"
    days = soup.find_all("div", class_=dayclass)
    for item in days:
        if item.text.find(request.text, 0, len(item.text)) != -1:
            # bot.send_message(message.chat.id, item.text)
            try:
                idx = item.text.index(request.text, 0, len(item.text))
                bot.send_message(request.chat.id, item.text.split()[0] + item.text.split()[1] +
                                 item.text.split()[2] + "\n" +
                                 item.text[idx:idx + 70].split('\n\n\n')[0] + " играет " +
                                 item.text[idx:idx + 70].split('\n\n\n')[1] + "\n")
                continue
            except:
                # bot.send_message(request.chat.id, item.text.split() + str(request.text) + "не играет\n")
                bot.send_message(request.chat.id, item.text.split()[0] + item.text.split()[1] +
                                 item.text.split()[2] + " " + request.text + " не играет\n")
                continue
        return
    # ------------------------------
    bot.send_message(request.chat.id, "У выбранной вами команды на данный момент больше нет матчей")
    return


def resultsearch(request):
    # Парсим -----------------------
    url = 'https://www.hltv.org/results'
    htmlcode = requests.get(url).text
    soup = BeautifulSoup(htmlcode, "lxml")
    resultclass = "results-sublist"
    days = soup.find_all("div", class_=resultclass)
    count = 0
    for item in days:
        if item.text.find(request.text, 0, len(item.text)) != -1:
            bot.send_message(request.chat.id, '\n\n\n'.join(item.text.split("\n\n\n\n\n\n\n\n\n\n\n")))
            return
        if count == 3:
            return
        count += 1
    # ------------------------------
    bot.send_message(request.chat.id, "В выбранной вами день матчи не проходили")
    return


bot.polling(none_stop=True)
