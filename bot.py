# bot.py
import telebot
from app import TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет! Я бот для конвертации валют. Для получения курса валют введите команду в формате:\n"
                                     "<имя валюты цену которой вы хотите узнать> "
                                     "<имя валюты, в которой надо узнать цену первой валюты> "
                                     "<количество первой валюты>\n\n"
                                     "Например: USD EUR 100")

@bot.message_handler(commands=['values'])
def handle_values(message):
    bot.send_message(message.chat.id, "Доступные валюты: USD, RUB")

@bot.message_handler(content_types=['text'])
def handle_convert(message):
    try:
        chat_id = message.chat.id
        text = message.text.split()
        if len(text) != 3:
            raise APIException("Неверный формат запроса. Введите команду согласно инструкции.")

        base, quote, amount = text[0], text[1], float(text[2])
        result = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(chat_id, f"Результат конвертации: {amount} {base} = {result} {quote}")

    except APIException as e:
        bot.send_message(chat_id, f"Ошибка: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
