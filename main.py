import re

import telebot
import requests

bot = telebot.TeleBot('1419482006:AAGGknahOOw07ZzSWDzjPChBf-z3pyuv0Fo')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    bot.send_message(chat_id,
                     'Привет, напиши мне слово, а я придумаю к нему рифму.')


@bot.message_handler(content_types=["text"])
def send_rhyme(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, 'твоё cлово: {}'.format(message.text))
    bot.send_message(chat_id, get_rhyme(message.text))


def get_rhyme(word):
    response = requests.get('https://rifmik.net/rhyme/{}'.format(word))
    word = ""
    try:
        index = response.text.find("<div class=\"results pad-1\">")
    except:
        word = "тааак, ищу, пока не придумал"
    try:
        index = response.text.find("<div id=\"syll2\" class=\"results pad-1\">")
    except:
        word = "Похоже я не знаю рифму к этому слову ;("
    if word == "":
        try:
            sum = response.text[index::].split("\r\n\r\n\t\t\t")[1]
            sum = re.split('<*>', sum)
            for i in range(1, len(sum)):
                word += sum[i].split("<")[0]
            return "рифма к нему: " + word
        except:
            return "Не придумал:("
    else:
        return word


if __name__ == '__main__':
    bot.polling(none_stop=True)
