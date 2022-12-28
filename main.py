import telebot
import sqlite3

from telebot.types import KeyboardButton, ReplyKeyboardMarkup

TOKEN = "5830674926:AAHtg3hps_NX9CF4YBtqSUgxtUnVDk1e8JU"

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def greetings(message):
    reply = "Я бот в котором вы можете узнать информацию о пациентах и добавить"
    bot.reply_to(message, reply, reply_markup=keyboard())


is_taking_name = False
is_taking_surname = False
user_name = None
surname = None


@bot.message_handler(content_types=['text'])
def message_handler(message):
    chat_id = message.chat.id
    global is_taking_name
    global is_taking_surname
    global user_name
    global surname

    if is_taking_surname == True:
        surname = message.text
        print(surname)
        is_taking_surname = False
        save_data_to_db(user_name, surname)

    if is_taking_name:
        user_name = message.text
        print(user_name)
        is_taking_name = False
        is_taking_surname = True
        bot.send_message(chat_id, "Выберите доктора:")

    if chat_id =='Выберите доктора':
        is_taking_name=True
        bot.send_message()


    if message.text == 'Добавить':
        is_taking_name = True
        bot.send_message(chat_id, "Напишите имя:")

    if message.text == 'Доктора':
        data = read_data_from_db()
        for datum in data:
            bot.reply_to(message, str(datum))

    if message.text == "Next":
        bot.reply_to(message, "Выберите имя пациента:", reply_markup=next_keyboard())

    if message.text == "Back":
        bot.reply_to(message, "Выберите имя пациента:", reply_markup=keyboard())


def save_data_to_db(name, surname):

    connection = None

    try:
        connection = sqlite3.connect("botdatabase")
        cursor = connection.cursor()

        inser_sql =f"""INSERT INTO
                    User (name, surname) 
                    VALUES ('{name}', '{surname}')"""

        cursor.execute(inser_sql)
        connection.commit()
        connection.close()

    except Exception as e:
        print("There was an error in the database!")


def read_data_from_db():
    try:
        connection = sqlite3.connect("botdatabase")
        cursor = connection.cursor()

        select_sql = """
        SELECT * FROM User
        """
        cursor.execute(select_sql)
        connection.commit()

        data = cursor.fetchall()

        connection.close()
        return data

    except Exception as e:
        print("There was an error with database!")
        print(e)


def keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button1 = KeyboardButton("Добавить")
    button2 = KeyboardButton("Доктора")
    button3 = KeyboardButton("Next")

    markup.add(button1, button2)
    markup.add(button3)

    return markup

def next_keyboard():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

    button1 = KeyboardButton("Ольга Бузова")
    button2 = KeyboardButton("Владимир Песков")
    button3 = KeyboardButton("Петр 1")
    button4 = KeyboardButton("Back")

    markup.add(button1, button2, button3)
    markup.add(button4)

    return markup

    if button1 == 'Ольга Бузова':
        is_taking_name = True
        bot.send_message(chat_id, "Записали 4 дня назад.Находится в 25 палате.Доктор:Стоматолог")
        return True




bot.infinity_polling()


