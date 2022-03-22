import telebot
from configuration import keys, TOKEN
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате через пробел:\n \
           <Название валюты>\n \
           <в какую валюту перевести>\n  \
           <колличество переводимой валюты>\n \
           <Чтобы увидеть спиок всех доступных валют введите: /values\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров!')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать запрос \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} -  {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

