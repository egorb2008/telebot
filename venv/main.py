import telebot
from telebot import types
import psycopg2
import datetime

token = "xxx"
bot = telebot.TeleBot(token)
connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="telebot")
cursor = connection.cursor()
@bot.message_handler(commands = ["start"]) # команда старт
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, нажми на кнопку или введи в ручную день, на который хотел бы увидеть расписание.', reply_markup=keyboard())

@bot.message_handler(commands = ['help'])
def start_message(message):
    bot.send_message(message.chat.id, "Я умею показывать твоё расписание. \nНа какой день ты бы хотел узнать расписание?")

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button1 = types.KeyboardButton('Понедельник')
    button2 = types.KeyboardButton('Вторник')
    button3 = types.KeyboardButton('Среда')
    button4 = types.KeyboardButton('Четверг')
    button5 = types.KeyboardButton('Пятница')
    button6 = types.KeyboardButton('Сайт МТУСИ')
    markup.add(button1, button2, button3, button4, button5, button6)
    return markup

def keyboardeven():
    buttn1 = types.KeyboardButton('Понедельник')
    buttn2 = types.KeyboardButton('Вторник')
    buttn3 = types.KeyboardButton('Среда')
    buttn4 = types.KeyboardButton('Четверг')
    buttn5 = types.KeyboardButton('Пятница')
    buttn6 = types.KeyboardButton('Сайт МТУСИ')
    markup2 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True).add(buttn1).add(buttn2).add(buttn3).add(buttn4).add(buttn5).add(buttn5).add(buttn6)
    return(markup2)

def keyboardodd():
    butn1 = types.KeyboardButton('Понедельник')
    butn2 = types.KeyboardButton('Вторник')
    butn3 = types.KeyboardButton('Среда')
    butn4 = types.KeyboardButton('Четверг')
    butn5 = types.KeyboardButton('Пятница')
    butn6 = types.KeyboardButton('Сайт МТУСИ')
    markup3 = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True).add(butn1).add(butn2).add(
        butn3).add(butn4).add(butn5).add(butn6)
    return markup3



def messageResult(lessons): # чтобы выводились все элементы
    main_list = []
    for i in lessons:
        main_list.append(' '.join(i))
    return(main_list)
@bot.message_handler(content_types = ['text'])
def manipulator(message):
    week = int(datetime.date.today().isocalendar()[1]) % 2  # чётная ли неделя
    flag = True
    day = 0
    if message.text == "Понедельник":
        day = 1
    elif message.text == "Вторник":
        day = 2
    elif message.text == "Среда":
         day = 3
    elif message.text == "Четверг":
        day = 4
    elif message.text == "Пятница":
        day = 5
    else:
        if message.text == "Сайт МТУСИ":
            flag = True
        else:
            flag = False
    if flag == True:
        if message.text == "Сайт МТУСИ":
            bot.send_message(message.chat.id, 'https://mtuci.ru/', reply_markup=keyboard())
        else:
            cursor.execute(f'SELECT timetable.subject, timetable.room_numb, timetable.start_time, teacher.full_name FROM timetable JOIN teacher ON timetable.teacher_id = teacher.id WHERE timetable.day = {day} and WEEK = {week} ORDER BY number;')
            lessons = cursor.fetchall()
            my_list = messageResult(lessons)
            my_str = '\n'.join(my_list)  # my_str принимает значение my_list как строки и переносит каждый элемент
            # на новую строку

            bot.send_message(message.chat.id, my_str, reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, "Я не понимаю что Вы от меня хотите. Используйте кнопки.")

bot.infinity_polling() # бесконечная работа бота