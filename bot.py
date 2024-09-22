import time
from telebot import TeleBot
from keyboard import *
from localization.lang import *

token = "7752906132:AAGAtoPZApvDMtgexWwMOjHHpekGV3QElAY"

bot = TeleBot(token)

user_data = {}
user_langs = {}

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    bot.send_message(chat_id, "Butunjahon Yoshlar Assotsiatsiyasining Misrdagi ofisiga Xush kelibsiz!", reply_markup=generate_language())
    bot.register_next_step_handler(message, choose_lang)


def choose_lang(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Quyidagilardan birini tanlang!", reply_markup=generate_main_menu())
    bot.register_next_step_handler(message, main_menu)


def main_menu(message):
    chat_id = message.chat.id
    photo = open("media/vision.png", 'rb')
    if message.text == "🎯 Biz haqimizda":
        bot.send_photo(chat_id, photo, caption="\n<b>MissiyaMissiya</b>: Biz yosh avlodga global imkoniyatlar yaratish orqali ularning shaxsiy va kasbiy rivojlanishiga hissa qo‘shishni maqsad qilganmiz."
                                               "\n<b>Vizyon</b>: Yoshlarning ta’lim, tadbirkorlik va ko‘ngillilik yo‘nalishlaridagi imkoniyatlarini kengaytirib, kelajakda muvaffaqiyatli yetakchilarni tarbiyalash.\n\nBizning jamoamiz xalqaro tajribaga ega, faol va iqtidorli yoshlar, tadbirkorlar hamda yetakchilardan iborat. "
                                               "Har bir jamoa a’zosi yoshlar o‘rtasida global hamkorlikni mustahkamlash va yangi imkoniyatlar yaratishda muhim rol o‘ynaydi.\n\n"
                                               "Tashkilotimiz 2000-yillarning boshida yoshlar almashinuvi dasturlarini rivojlantirish va yosh avlodga xalqaro miqyosda yangi imkoniyatlar yaratish maqsadida tashkil topgan. Bugungi kunda, biz minglab yoshlarni global platformalarda muvaffaqiyatli ishtirok etishlariga ko‘maklashib kelmoqdamiz.",
                                                parse_mode="HTML", reply_markup=generate_back())
        bot.register_next_step_handler(message, back)



    elif message.text == "💬 Biz bilan bog‘laning":
        bot.send_message(chat_id, "\nAloqa ma’lumotlari:\n\nTelefon raqamlari: +998991234567\n"
                                  "Elektron pochta: example@gmail.com\n"
                                  "Manzillari: Nil bo’yi\n"
                                  "Ofis vaqtlari: 09:00 – 18:00.", reply_markup=generate_connect())
        bot.register_next_step_handler(message, connect)

    elif message.text == "🌐 Ijtimoiy tarmoqlar":
        bot.send_message(chat_id, message.text)

    elif message.text == "📑 Yangiliklar va E'lonlar":
        bot.send_message(chat_id, message.text)

    elif message.text == "📝 So‘rov va Fikr-mulohaza":
        bot.send_message(chat_id, message.text)

    elif message.text == "📊 Yoshlar uchun resurslar":
        bot.send_message(chat_id, message.text)

    elif message.text == "Tilni o'zgartirish":
        bot.send_message(chat_id, "Tilni tanlang!",
                         reply_markup=generate_language())
        bot.register_next_step_handler(message, choose_lang)

def connect(message):
    chat_id = message.chat.id
    if message.text == "Bizning Geolokatsiya":
        bot.send_message(chat_id, 'Bizning Geolokatsiya')
        bot.send_location(chat_id, latitude=40.86091, longitude=69.58965, reply_markup=generate_back())
        bot.register_next_step_handler(message, back_connect)

    elif message.text == "Savol/Taklif yuborish":
        bot.send_message(chat_id, "F.I.O yuboring: ")
        bot.register_next_step_handler(message, user_email)


    elif message.text == "Orqaga":
        return back(message)



def user_email(message):
    fio = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, "Elektron pochtangizni yuboring: ")
    bot.register_next_step_handler(message, user_question,fio)


def user_question(message, fio):
    email = message.text
    chat_id = message.chat.id
    if "@" in email:
        bot.send_message(chat_id, "Savol/Taklifingizni yuboring: ")
        bot.register_next_step_handler(message, user_phone,  fio, email)

    else:
        bot.send_message(chat_id, "Elektron pochta xato kiritildi.\nPochtangizni qaytadan yuboring!")
        time.sleep(1)
        bot.send_message(chat_id, "Elektron pochtangizni yuboring: ")
        bot.register_next_step_handler(message, user_question, fio)


def user_phone(message, fio, email):
    quest = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id, "Tel raqamingizni +998 ** *** ** ** korinishida yuboring: ", reply_markup=contact())
    bot.register_next_step_handler(message, send_group_message, fio, quest, email)


def send_group_message(message, fio, quest, email):
    chat_id = message.chat.id
    if message.text:
        phone = message.text
        bot.send_message(chat_id, f"Tasdiqlaysizmi?!\nF.I.O:{fio}\n"
                                  f"Elektron pochtangiz: {email}\n"
                                  f"Savol/Taklifingiz: {quest}\n"
                                  f"Tel raqamingiz: {phone}", reply_markup=commit())
        bot.register_next_step_handler(message, message_commit, fio, email, quest, phone)

    elif message.contact:
        phone = message.contact.phone_number
        bot.send_message(chat_id, f"Tasdiqlaysizmi?!\nF.I.O:{fio}\n"
                                  f"Elektron pochtangiz: {email}\n"
                                  f"Savol/Taklifingiz: {quest}\n"
                                  f"Tel raqamingiz: {phone}", reply_markup=commit())
        bot.register_next_step_handler(message, message_commit, fio, email, quest, phone)
def message_commit(message, fio, email, quest, phone):
    chat_id = message.chat.id
    if message.text == 'Ha':
        bot.send_message(chat_id, "Ma'lumotlar qabul qilindi!")
        bot.send_message(-1002348352534, f"Tasdiqlaysizmi?!\nF.I.O:{fio}\n"
                                  f"Elektron pochtangiz: {email}\n"
                                  f"Savol/Taklifingiz: {quest}\n"
                                  f"Tel raqamingiz: {phone}")
        time.sleep(3)
        bot.send_message(chat_id, "Quyidagilardan birini tanlang!", reply_markup=generate_main_menu())
        bot.register_next_step_handler(message, main_menu)

    elif message.text == "Yo'q":
        bot.send_message(chat_id, "\nAloqa ma’lumotlari:\n\nTelefon raqamlari: +998991234567\n"
                                  "Elektron pochta: example@gmail.com\n"
                                  "Manzillari: Nil bo’yi\n"
                                  "Ofis vaqtlari: 09:00 – 18:00.", reply_markup=generate_connect())
        bot.register_next_step_handler(message, connect)





def back_connect(message):
    chat_id = message.chat.id
    if message.text == "Orqaga":
        bot.send_message(chat_id, "\nAloqa ma’lumotlari:\n\nTelefon raqamlari: +998991234567\n"
                                  "Elektron pochta: example@gmail.com\n"
                                  "Manzillari: Nil bo’yi\n"
                                  "Ofis vaqtlari: 09:00 – 18:00.", reply_markup=generate_connect())
        bot.register_next_step_handler(message, connect)


def back(message):
    if message.text == "Orqaga":
        return choose_lang(message)


bot.polling(non_stop=True)