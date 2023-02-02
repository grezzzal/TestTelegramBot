import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConvector

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Этот бот был создан для конвертации из одной валюты в другую\n\n' \
           'Чтобы начать работу введите команду боту в следующем формате:\n' \
           '<Имя валюты>\n' \
           '<В какую валюту конвертировать>\n' \
           '<Количество конвертируемой валюты>\n\n' \
           'Чтобы узнать список доступных валют введите /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Неверное кол-во значений')

        base, quote, amount = value
        d = ValueConvector.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера\n{e}')
    else:
        text = f'{amount} {quote} равно {d} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
