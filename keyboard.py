from telebot import types


def generate_language():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_uz = types.KeyboardButton(text="Uz")
    btn_ar = types.KeyboardButton(text="Ar")
    btn_en = types.KeyboardButton(text="En")
    btn_gr = types.KeyboardButton(text="Gr")
    btn_fr = types.KeyboardButton(text="Fr")
    keyboard.row(btn_uz, btn_ar, btn_en, btn_gr, btn_fr)
    return keyboard


def generate_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_about = types.KeyboardButton(text="🎯 Biz haqimizda")
    btn_connect = types.KeyboardButton(text="💬 Biz bilan bog‘laning")
    btn_social = types.KeyboardButton(text="🌐 Ijtimoiy tarmoqlar")
    btn_news = types.KeyboardButton(text="📑 Yangiliklar va E'lonlar")
    btn_idea = types.KeyboardButton(text="📝 So‘rov va Fikr-mulohaza")
    btn_data = types.KeyboardButton(text="📊 Yoshlar uchun resurslar")
    btn_back = types.KeyboardButton(text="Tilni o'zgartirish")
    keyboard.row(btn_about,btn_connect)
    keyboard.row(btn_social,btn_news)
    keyboard.row(btn_idea,btn_data)
    keyboard.row(btn_back)
    return keyboard


def generate_back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_back = types.KeyboardButton(text="Orqaga")
    keyboard.row(btn_back)
    return keyboard


def generate_connect():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_quest = types.KeyboardButton(text="Savol/Taklif yuborish")
    btn_location = types.KeyboardButton(text="Bizning Geolokatsiya")
    btn_back = types.KeyboardButton(text="Orqaga")
    keyboard.row(btn_quest, btn_location)
    keyboard.row(btn_back)
    return keyboard



def commit():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_quest = types.KeyboardButton(text="Ha")
    btn_location = types.KeyboardButton(text="Yo'q")
    keyboard.row(btn_quest, btn_location)
    return keyboard


def contact():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text="Kontakt yuborish", request_contact=True)
    keyboard.row(btn)
    return keyboard