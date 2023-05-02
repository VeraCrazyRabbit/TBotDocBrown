import os
import random
import json
import logging
import telebot

from settings import BOT_TOKEN

from telebot import types

bot = telebot.TeleBot(os.environ.get(BOT_TOKEN))

user_game = {}


# --------------------- bot ---------------------

# --------------- start/help --------------------
@bot.message_handler(commands=['start'])
def start(message):
    m = 'CAACAgEAAxkBAAEE7rxin5-boWU22IzZGSczBm4OfkLqkAAC5gADWiSJRtvzAtn5dWoEJAQ'
    mess = f'Добро пожаловать в ✨Новый Вектор✨\n\nМеня зовут Мастер Сплинтер и я буду направлять тебя на этом пути! 😌'
    bot.send_sticker(message.chat.id, m)
    bot.send_message(message.chat.id, mess)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    h = types.KeyboardButton('/startgamer')
    s = types.KeyboardButton('/startadmin')
    markup.add(h, s)
    bot.send_message(message.chat.id, 'Выбери свою роль: игрок или админиcтратор!', reply_markup=markup)


# ---------------- ADMIN -----------------------
@bot.message_handler(commands=['startadmin'])
def start(message):
    m = 'Приветствую тебя геймификатор!'
    s = 'CAACAgIAAxkBAAEE4SZilS7MDpKmnr8lv_b5BvYSlPn8uwACrBMAAjieIUvRyGVa6d742yQE'
    mess = 'Введи секретный пароль'
    bot.send_message(message.chat.id, m)
    bot.send_sticker(message.chat.id, s)
    msg = bot.send_message(message.chat.id, mess, reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_verify)


def get_verify(message):
    if message.text == 'password':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text != '/mainmenu':
        msg = bot.send_message(message.chat.id,
                               'Не верный пароль!\nПопробуй еще раз или ты обманщик-игрок и тебе пора в /mainmenu? 😑')
        bot.register_next_step_handler(msg, get_verify)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        h = types.KeyboardButton('/startgamer')
        s = types.KeyboardButton('/startadmin')
        markup.add(h, s)
        bot.send_message(message.chat.id, 'Выбери свою роль: игрок или админиcтратор!', reply_markup=markup)


# ---------------- GAMER -----------------------
@bot.message_handler(commands=['startgamer'])
def start_gamer(message):
    m = 'Приветствую тебя игрок!'
    s = f'CAACAgEAAxkBAAEE7t9in7Tm86pe0BEJyeqX08umkx34wwACxgADFC-IRr9WJ3-by2R_JAQ'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    h = types.KeyboardButton('/helpgamer')
    s = types.KeyboardButton('/signup')
    g = types.KeyboardButton('/game')
    a = types.KeyboardButton('/mainmenu')
    l = types.KeyboardButton('/statistic')
    markup.add(h, s, g, l, a)
    bot.send_message(message.chat.id, m)
    # bot.send_sticker(message.chat.id, s)
    bot.send_message(message.chat.id, 'Чем я могу помочь? 🙂\n/helpgamer', reply_markup=markup)


@bot.message_handler(commands=['helpgamer'])
def help_gamer(message):
    global user_game
    mess = '🧐 Что я могу: 🔎'
    m1 = f'/signup - Регистрация нового персонажа'
    m2 = f'/statistic - Посмотреть статистику по своему персонажу'
    m3 = f'/game - Ежедневная загадка'
    m4 = f'/exit - Выход в меню игрока'
    m5 = f'/mainmenu - Выход в главное меню'
    bot.send_message(message.chat.id, mess + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4 + '\n' + m5)
    bot.send_message(message.chat.id, user_game)


# ---------------- signup ----------------------

@bot.message_handler(commands=['signup'])
#          ------ name -------
def ButSignUp(message):
    bot.send_message(message.chat.id, '👾 Добро пожаловать в раздел регистрации!')
    bot.send_message(message.chat.id, 'Создай своего персонажа 🧍и отправляйся в увлекательное приключение 🤩')
    bot.send_message(message.chat.id, 'Введи Фамилию и Имя')
    msg = bot.send_message(message.chat.id, 'Вводи корректные данные, иначе я не смогу начислять тебе баллы',
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_password)


#          ------ password -------
def get_password(message):
    global user_game
    name = message.text
    if name not in user_game:
        user_game[name] = {}
        msg = bot.send_message(message.chat.id,
                               'Придумай пароль 🔒\nЗапомни его, после ввода он исчезнет. Узнать его ты сможешь только у геймификатора.')
        bot.register_next_step_handler(msg, get_area, name)
    else:
        bot.send_message(message.chat.id,
                         'Такой пользователь уже создан 🤷. Начни регистрацию заново /signup или нажми /statistic, чтобы посмотреть статистику.')


#          ------ area -------
def get_area(message, name_user):
    global user_game
    password = message.text
    user_game[name_user]['password'] = password
    bot.delete_message(message.chat.id, message.message_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    area1 = types.KeyboardButton('ЦАО ❤')
    area2 = types.KeyboardButton('СЗАО 🖤')
    area3 = types.KeyboardButton('САО 💚')
    area4 = types.KeyboardButton('ЗелАО 💙')
    area5 = types.KeyboardButton('СВАО 💜')
    area6 = types.KeyboardButton('ВАО 💛')
    markup.add(area1, area2, area3, area4, area5, area6)
    msg = bot.send_message(message.chat.id, 'Выберите округ 🌍', reply_markup=markup)
    bot.register_next_step_handler(msg, get_name, name_user)


#          ------ verify -------
def get_name(message, name_user):
    global user_game
    user_game[name_user]['area'] = message.text
    area = user_game[name_user]['area']
    mess = f'Ты из {area}. Тебя зовут {name_user}. Все верно?'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton('Да')
    no = types.KeyboardButton('Нет')
    markup.add(yes, no)
    msg = bot.send_message(message.from_user.id, mess, reply_markup=markup)
    bot.register_next_step_handler(msg, get_yn, name_user)


#          ------ persons -------
def get_yn(message, name_user):
    global user_game
    if message.text == 'Нет':
        del user_game[name_user]
        bot.register_next_step_handler(msg, Exit)
    elif message.text == 'Да':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        area1 = types.KeyboardButton('Ниндзя 🥷')
        area2 = types.KeyboardButton('Фея 🧚')
        area3 = types.KeyboardButton('Сыщик 🕵')
        area4 = types.KeyboardButton('Эльф 🧝')
        area5 = types.KeyboardButton('Русалка 🧜')
        area6 = types.KeyboardButton('Вампир 🧛')
        markup.add(area1, area2, area3, area4, area5, area6)
        msg = bot.send_message(message.chat.id, 'Выбери персонажа 🧍(именно он будет отображаться у тебя в дальнейшем)',
                               reply_markup=markup)
        bot.register_next_step_handler(msg, finish_reg, name_user)


#          ------ result  -------
def finish_reg(message, name_user):
    global user_game
    user_game[name_user]['pers'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    h = types.KeyboardButton('/helpgamer')
    s = types.KeyboardButton('/signup')
    g = types.KeyboardButton('/game')
    a = types.KeyboardButton('/exit')
    l = types.KeyboardButton('/statistic')
    markup.add(h, s, g, l, a)
    bot.send_message(message.chat.id, 'Поздравляю! Ты зарегистрирован!😎', reply_markup=markup)
    user_game[name_user]['money'] = 0
    user_game[name_user]['level'] = 0
    user_game[name_user]['stat'] = 'Новичок'
    area = user_game[name_user]['area']
    pers = user_game[name_user]['pers']
    money = user_game[name_user]['money']
    level = user_game[name_user]['level']
    stat = user_game[name_user]['stat']
    pas = user_game[name_user]['password']
    bot.send_message(message.chat.id,
                     f'{name_user}\n{pas}\n🌍:   {area}\n🧍:   {pers}\n💰:   {money}\n📊:   {level}\n🏆:   {stat}')


# ----------------- statistic ------------------------

@bot.message_handler(commands=['statistic'])
def ButLogin(message):
    msg = bot.send_message(message.chat.id, 'Введи Фамилию и Имя и я покажу твою статистику 🤑',
                           reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, PassWord)


def PassWord(message):
    global user_game
    name = message.text
    if name in user_game:
        msg = bot.send_message(message.chat.id, 'Введи пароль 🔒')
        bot.register_next_step_handler(msg, MyStat, name)
    else:
        bot.send_message(message.chat.id, 'Такой персонаж не найден 😢\nЗарегистрируйся /signup')


def MyStat(message, name_user):
    global user_game
    if message.text == user_game[name_user]['password']:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        h = types.KeyboardButton('/helpgamer')
        s = types.KeyboardButton('/signup')
        g = types.KeyboardButton('/game')
        a = types.KeyboardButton('/exit')
        l = types.KeyboardButton('/statistic')
        markup.add(h, s, g, l, a)
        area = user_game[name_user]['area']
        pers = user_game[name_user]['pers']
        money = user_game[name_user]['money']
        level = user_game[name_user]['level']
        stat = user_game[name_user]['stat']
        bot.send_message(message.chat.id,
                         f'{name_user}\n🌍:   {area}\n🧍:   {pers}\n💰:   {money}\n📊:   {level}\n🏆:   {stat}',
                         reply_markup=markup)
    elif message.text != '/exit':
        msg = bot.send_message(message.chat.id, 'Не верный пароль 🤐\nПопробуй еще раз или нажми /exit')
        bot.register_next_step_handler(msg, MyStat, name_user)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        h = types.KeyboardButton('/helpgamer')
        s = types.KeyboardButton('/signup')
        g = types.KeyboardButton('/game')
        a = types.KeyboardButton('/mainmenu')
        l = types.KeyboardButton('/statistic')
        markup.add(h, s, g, l, a)
        bot.send_message(message.chat.id, 'Чем я могу помочь? 🙂\n/helpgamer', reply_markup=markup)


# ------------------- exit ----------------------
@bot.message_handler(commands=['exit'])
def Exit(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    h = types.KeyboardButton('/helpgamer')
    s = types.KeyboardButton('/signup')
    g = types.KeyboardButton('/game')
    a = types.KeyboardButton('/mainmenu')
    l = types.KeyboardButton('/statistic')
    markup.add(h, s, g, l, a)
    bot.send_message(message.chat.id, 'Чем я могу помочь? 🙂\n/helpgamer', reply_markup=markup)


# ---------------- MAIN MENU --------------------
@bot.message_handler(commands=['mainmenu'])
def MainMenu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    h = types.KeyboardButton('/startgamer')
    s = types.KeyboardButton('/startadmin')
    markup.add(h, s)
    bot.send_message(message.chat.id, 'Выбери свою роль: игрок или админиcтратор!', reply_markup=markup)


# ------------------- DIALOG --------------------
@bot.message_handler(content_types=['text'])
def Mess(message):
    bot.send_message(message.chat.id, 'Я тебя не понимаю. Используй команду /exit')


# ---------------- local testing ----------------
if __name__ == '__main__':
    bot.infinity_polling()
