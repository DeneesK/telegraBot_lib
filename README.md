## simple bot example:

from telebot import Bot


bot = Bot("5333268354:AAF8Cj_P9OzF3cSdULLOBWpnSTdX48c3blI")


@bot.message_handler()
def main(message):
    if message.text == 'HI':
        bot.send_message(text="Hi there!", 
                         chat_id=message.chat["id"])


@bot.message_handler()
def next(message):
    if message.text == 'whoami':
        bot.send_message(text="bot", 
                         chat_id=message.chat["id"])


if __name__ == "__main__":
    bot.run()