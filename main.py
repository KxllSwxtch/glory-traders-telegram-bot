import locale
import asyncio
import threading

from telebot import types
from calculator import (
    calculate_cost,
    get_currency_rates,
    show_country_selection,
    get_nbk_currency_rates,
    get_nbkr_currency_rates,
)
from config import bot


# Переменные
user_data = {}

# Set locale for number formatting
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == "calculate_another":
        # user_data[call.message.chat.id] = {}  # Сброс страны
        show_country_selection(call.message.chat.id)


# Функция для установки команд меню
def set_bot_commands():
    commands = [
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("cbr", "Курс ЦБ Российской Федерации"),
        types.BotCommand("nbk", "Курс Национального Банка Республики Казахстан"),
        types.BotCommand("nbkr", "Курс Национального Банка Республики Кыргызстан"),
    ]
    bot.set_my_commands(commands)


@bot.message_handler(commands=["nbkr"])
def nbkr_command(message):
    try:
        rates_text = get_nbkr_currency_rates()

        # Создаем клавиатуру с кнопкой для расчета автомобиля
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                "🔍 Рассчитать стоимость автомобиля", callback_data="calculate_another"
            )
        )

        # Отправляем сообщение с курсами и клавиатурой
        bot.send_message(message.chat.id, rates_text, reply_markup=keyboard)
    except Exception as e:
        bot.send_message(
            message.chat.id, "Не удалось получить курсы валют. Попробуйте позже."
        )
        print(f"Ошибка при получении курсов валют: {e}")


@bot.message_handler(commands=["nbk"])
def nbk_command(message):
    try:
        rates_text = get_nbk_currency_rates()

        # Создаем клавиатуру с кнопкой для расчета автомобиля
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                "🔍 Рассчитать стоимость автомобиля", callback_data="calculate_another"
            )
        )

        # Отправляем сообщение с курсами и клавиатурой
        bot.send_message(message.chat.id, rates_text, reply_markup=keyboard)
    except Exception as e:
        bot.send_message(
            message.chat.id, "Не удалось получить курсы валют. Попробуйте позже."
        )
        print(f"Ошибка при получении курсов валют: {e}")


@bot.message_handler(commands=["cbr"])
def cbr_command(message):
    try:
        rates_text = get_currency_rates()

        # Создаем клавиатуру с кнопкой для расчета автомобиля
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton(
                "🔍 Рассчитать стоимость автомобиля", callback_data="calculate_another"
            )
        )

        # Отправляем сообщение с курсами и клавиатурой
        bot.send_message(message.chat.id, rates_text, reply_markup=keyboard)
    except Exception as e:
        bot.send_message(
            message.chat.id, "Не удалось получить курсы валют. Попробуйте позже."
        )
        print(f"Ошибка при получении курсов валют: {e}")


# Самый старт
@bot.message_handler(commands=["start"])
def start(message):
    user_name = message.from_user.first_name

    # Приветственное сообщение
    greeting = f"👋 Здравствуйте, {user_name}!\n Я бот компании Glory Traders для расчета стоимости авто из Южной Кореи до стран СНГ! 🚗 \n\n💰 Пожалуйста, выберите действие из меню ниже:"

    # Создание кнопочного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_calc = types.KeyboardButton("Расчёт")
    btn_instagram = types.KeyboardButton("Instagram")
    btn_whatsapp = types.KeyboardButton("WhatsApp")
    btn_telegram = types.KeyboardButton("Telegram-канал")
    btn_manager = types.KeyboardButton("Написать менеджеру")

    # Добавление кнопок в меню
    markup.add(btn_calc, btn_instagram, btn_whatsapp, btn_telegram, btn_manager)

    # Отправка приветствия с кнопочным меню
    bot.send_message(message.chat.id, greeting, reply_markup=markup)


# Главное меню
@bot.message_handler(func=lambda message: message.text == "Вернуться в главное меню")
def main_menu(message):
    # Приветственное сообщение
    user_name = message.from_user.first_name
    greeting = f"👋 Здравствуйте, {user_name}!\n Я бот компании Glory Traders для расчета стоимости авто из Южной Кореи до стран СНГ! 🚗 \n\n💰 Пожалуйста, выберите действие из меню ниже:"

    # Создание кнопочного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_calc = types.KeyboardButton("Расчёт")
    btn_instagram = types.KeyboardButton("Instagram")
    btn_whatsapp = types.KeyboardButton("WhatsApp")
    btn_telegram = types.KeyboardButton("Telegram-канал")
    btn_manager = types.KeyboardButton("Написать менеджеру")

    # Добавление кнопок в меню
    markup.add(btn_calc, btn_instagram, btn_whatsapp, btn_telegram, btn_manager)

    # Отправка приветствия с кнопочным меню
    bot.send_message(message.chat.id, greeting, reply_markup=markup)


# Выбор страны для расчёта
@bot.message_handler(func=lambda message: message.text in ["Расчёт", "Изменить страну"])
def handle_calculation(message):
    show_country_selection(message.chat.id)


# Расчёт по ссылке с encar
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def process_encar_link(message):
    # Проверяем, выбрана ли страна
    if message.chat.id not in user_data or "country" not in user_data[message.chat.id]:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите страну из меню перед отправкой ссылки на автомобиль.",
        )
        return

    # Проверяем, что ссылка содержит encar.com или fem.encar.com
    if "encar.com" not in message.text or "fem.encar.com" not in message.text:
        bot.send_message(
            message.chat.id,
            "🚫 Введите корректную ссылку с encar.com",
        )
        return

    # Получаем выбранную страну
    country = user_data[message.chat.id]["country"]

    # Отправляем сообщение о начале обработки
    processing_message = bot.send_message(message.chat.id, "⏳ Обработка данных...")

    # Пытаемся рассчитать стоимость
    try:
        calculate_cost(country, message)
    except Exception as e:
        bot.send_message(
            message.chat.id,
            "🚫 Произошла ошибка при расчёте. Пожалуйста, попробуйте снова.",
        )
        print(f"Ошибка при расчёте: {e}")
    finally:
        # Удаляем сообщение о процессе
        bot.delete_message(message.chat.id, processing_message.message_id)


@bot.message_handler(func=lambda message: message.text == "По ссылке с encar")
def handle_link_input(message):
    bot.send_message(
        message.chat.id,
        "Отправьте ссылку на автомобиль с сайта encar.com или мобильного приложения Encar.",
    )


# Ручной расчёт
@bot.message_handler(func=lambda message: message.text == "Ручной ввод")
def handle_manual_input(message):
    bot.send_message(
        message.chat.id,
        "Пожалуйста, укажите данные автомобиля для расчёта:\n\n"
        "Год выпуска, объём двигателя, цена в Корее (в вонах) (например: 2022 2497cc 25000000).",
    )


###############
# РОССИЯ НАЧАЛО
###############
@bot.message_handler(func=lambda message: message.text == "🇷🇺 Россия")
def handle_russia(message):
    user_data[message.chat.id] = {"country": "Russia"}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_link = types.KeyboardButton("По ссылке с encar")
    btn_manual = types.KeyboardButton("Ручной ввод")
    btn_main_menu = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn_link, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выберите способ расчёта:",
        reply_markup=markup,
    )


###############
# РОССИЯ КОНЕЦ
###############


##############
# КАЗАХСТАН НАЧАЛО
##############
@bot.message_handler(func=lambda message: message.text == "🇰🇿 Казахстан")
def handle_kazakhstan(message):
    user_data[message.chat.id] = {"country": "Kazakhstan"}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_link = types.KeyboardButton("По ссылке с encar")
    btn_manual = types.KeyboardButton("Ручной ввод")
    btn_main_menu = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn_link, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выберите способ расчёта:",
        reply_markup=markup,
    )


##############
# КАЗАХСТАН КОНЕЦ
##############


##############
# КЫРГЫЗСТАН НАЧАЛО
##############
@bot.message_handler(func=lambda message: message.text == "🇰🇬 Кыргызстан")
def handle_kyrgyzstan(message):
    user_data[message.chat.id] = {"country": "Kyrgyzstan"}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_link = types.KeyboardButton("По ссылке с encar")
    btn_manual = types.KeyboardButton("Ручной ввод")
    btn_main_menu = types.KeyboardButton("Вернуться в главное меню")
    markup.add(btn_link, btn_manual, btn_main_menu)

    bot.send_message(
        message.chat.id,
        "Выберите способ расчёта:",
        reply_markup=markup,
    )


##############
# КЫРГЫЗСТАН КОНЕЦ
##############


# Обработчики для других кнопок
@bot.message_handler(func=lambda message: message.text == "Instagram")
def handle_instagram(message):
    bot.send_message(
        message.chat.id,
        "Наш Instagram: https://www.instagram.com/glory_traders_",
    )


@bot.message_handler(func=lambda message: message.text == "WhatsApp")
def handle_whatsapp(message):
    bot.send_message(
        message.chat.id, "Напишите нам в WhatsApp: https://wa.me/821023297807"
    )


@bot.message_handler(func=lambda message: message.text == "Telegram-канал")
def handle_telegram_channel(message):
    bot.send_message(
        message.chat.id,
        "Наш Telegram-канал: https://t.me/GLORYTRADERS",
    )


@bot.message_handler(func=lambda message: message.text == "Написать менеджеру")
def handle_manager(message):
    bot.send_message(message.chat.id, "Напишите нам напрямую: @GLORY_TRADERS")


def run_in_thread(target):
    """Запуск функции в отдельном потоке"""
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    # Запуск длительных задач в отдельных потоках
    run_in_thread(set_bot_commands)
    run_in_thread(get_nbkr_currency_rates)
    run_in_thread(get_nbk_currency_rates)
    run_in_thread(get_currency_rates)

    # Основной поток выполняет бот
    bot.polling(none_stop=True)
