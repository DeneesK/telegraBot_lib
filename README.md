## simple bot example:

```
from telebot import Bot


bot = Bot("<TOKEN>")


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