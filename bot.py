import os
import time
from datetime import datetime
import schedule
from telebot import TeleBot
from db.users_id import UserIDsDB
from keyboard import *
from localization.lang import *
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TOKEN")

bot = TeleBot(token)

user_data = {}
user_langs = {}
personal_details = {}
canal_id = os.getenv("CANAL_ID")
group_id = os.getenv("GROUP_ID")
instagram_link = os.getenv("INSTAGRAM_URL")
facebook_link = os.getenv("FACEBOOK_URL")
youtube_link = os.getenv("YOUTUBE_URL")
twitter_link = os.getenv("TWITTER_URL")
db = UserIDsDB()


@bot.message_handler(func=lambda message: True)
def testing(message):

    if message.text == '/start':
        return start(message)

    if message.text == '/admin':
        return admin(message)

#--------------------------------------Admin panel--------------------------------------
# Adminlarning ID ro'yxati
admin_id = list(map(int, os.getenv("ADMIN_ID").split(',')))

@bot.message_handler(commands=["admin"])
def admin(message):
    chat_id = message.chat.id
    if chat_id in admin_id:
        bot.send_message(chat_id, "Admin panelga xush kelibsiz!", reply_markup=admin_panel_markup())
        bot.register_next_step_handler(message, handle_admin_panel)
    else:
        bot.send_message(chat_id, "Siz admin emassiz!")

@bot.message_handler(func=lambda message: message.chat.id in admin_id)
def handle_admin_panel(message):
    chat_id = message.chat.id

    if message.text == "Yangilik qo'shish":
        create_news = bot.send_message(chat_id, "Yangilik ni yuboring")
        bot.register_next_step_handler(create_news, send_announcement)

    elif message.text == "Bo'limlarni ko'rish":
        bot.send_message(chat_id, "Bu bo'lim vaqtinchalik ishlamaydi.")
        time.sleep(1)
        bot.send_message(chat_id, "Bo'limlardan birini tanlang", reply_markup=admin_panel_markup())

@bot.message_handler(content_types=["photo", "text"])
def send_announcement(message):
    chat_id = message.chat.id

    if chat_id in admin_id:  # Faqat adminlarga ruxsat
        if message.content_type == "photo":
            # Rasm va captionni olish
            photo_id = message.photo[-1].file_id
            caption = message.caption if message.caption else "📢 Yangilik!"

            # Foydalanuvchilarga yuborish
            users = db.get_all_users()

            if users:
                for user_id in users:
                    try:
                        bot.send_photo(user_id, photo_id, caption=caption)
                    except Exception as e:
                        print(f"Xatolik {user_id} ga yuborishda: {e}")
                bot.send_message(chat_id, "📸 Rasmli yangilik muvaffaqiyatli yuborildi!")
                bot.send_message(chat_id, "bo'limlardan birini tanlang", reply_markup=admin_panel_markup())
            else:
                bot.send_message(chat_id, "Hozircha foydalanuvchilar ro'yxati bo'sh.")

        elif message.content_type == "text":
            # Textli yangilikni olish
            news_text = message.text

            # Foydalanuvchilarga yuborish
            users = db.get_all_users()

            if users:
                for user_id in users:
                    try:
                        bot.send_message(user_id, news_text)
                    except Exception as e:
                        print(f"Xatolik {user_id} ga yuborishda: {e}")
                bot.send_message(chat_id, "✉️ Textli yangilik muvaffaqiyatli yuborildi!")
                bot.send_message(chat_id, "bo'limlardan birini tanlang", reply_markup=admin_panel_markup())
            else:
                bot.send_message(chat_id, "Hozircha foydalanuvchilar ro'yxati bo'sh.")
    else:
        bot.send_message(chat_id, "⛔ Siz admin emassiz, yangilik yuborolmaysiz!")


#-------------------------------------Start------------------------------------------

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    db.insert_user(chat_id)  # Foydalanuvchi ID'sini saqlaymiz
    photo = open("media/start_image.jpg", "rb")
    bot.send_photo(chat_id, photo, start_message[lang], reply_markup=generate_language())


@bot.callback_query_handler(func=lambda call: call.data in ["uz", "ar","en", "gr","fr"])
def language(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if call.data == "uz":
        lang = "uz"

    elif call.data == "ar":
        lang = "ar"

    elif call.data == "en":
        lang = "en"

    elif call.data == "gr":
        lang = "gr"

    elif call.data == "fr":
        lang = "fr"


    bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))

    bot.register_next_step_handler(call.message, main_menu)
    user_langs[chat_id] = lang


def main_menu(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    photo = open("media/vision.png", 'rb')
    if message.text == about_bot[lang]:
        bot.send_photo(chat_id, photo, caption=about_caption[lang],
                                                parse_mode="HTML", reply_markup=generate_back(lang))
        bot.register_next_step_handler(message, back)


    elif message.text == connect_lang[lang]:
        bot.send_message(chat_id, connect_line_text[lang], reply_markup=generate_connect(lang))
        bot.register_next_step_handler(message, connect)


    elif message.text == network[lang]:
        bot.send_message(chat_id, text_network[lang], reply_markup=socialmedia(lang, facebook_link, instagram_link, twitter_link, youtube_link))
        bot.register_next_step_handler(message, back)

    elif message.text == news_lang[lang]:
        bot.send_message(chat_id, news_lang[lang], reply_markup=globalopportunities(lang))
        bot.register_next_step_handler(message, news)

    elif message.text == competitions[lang]:
        bot.send_message(chat_id, chalange[lang])
        time.sleep(1)
        bot.send_message(chat_id, category[lang], reply_markup=generate_main_menu(lang))
        # bot.send_photo(chat_id, photo, caption=siyrat_lang[lang], reply_markup=generate_challange(lang))


    elif message.text == resurs_lang[lang]:
        bot.send_message(chat_id, message.text, reply_markup=generate_resource(lang))
        bot.register_next_step_handler(message, news)


    elif message.text == change_lang[lang]:
        return start(message)



def connect(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text == location[lang]:
        bot.send_message(chat_id, location[lang])
        bot.send_location(chat_id, latitude=40.86091, longitude=69.58965, reply_markup=generate_back(lang))
        bot.register_next_step_handler(message, back_connect)

    elif message.text == quest_lang[lang]:
        bot.send_message(chat_id, question_lang[lang])
        bot.register_next_step_handler(message, user_name)


    elif message.text == back_lang[lang]:
        return back(message)

def user_name(message):
    quest = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, fio_lang[lang])
    bot.register_next_step_handler(message, user_question, quest)

def user_question(message, quest):
    name = message.text
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, phone_number_lang[lang], reply_markup=contact(lang))
    bot.register_next_step_handler(message, send_group_message, name, quest)

def send_group_message(message, name, quest):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text:
        phone = message.text
        personal_details['name'] = name
        personal_details['quest'] = quest
        personal_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {name}\n"
                                  f"{quest_offer_lang[lang]}{quest}\n"
                                  f"{user_phone_number_lang[lang]} {phone}", reply_markup=commit(lang))

    elif message.contact:
        phone = message.contact.phone_number
        personal_details['name'] = name
        personal_details['quest'] = quest
        personal_details['phone'] = phone
        bot.send_message(chat_id, f"{confirm_lang[lang]} {name}\n"
                                  f"{quest_offer_lang[lang]}{quest}\n"
                                  f"{user_phone_number_lang[lang]} {phone}", reply_markup=commit(lang))


@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def message_commit(call):
    chat_id = call.message.chat.id
    name = personal_details['name']
    quest = personal_details['quest']
    phone = personal_details['phone']
    lang = user_langs.get(chat_id, "uz")

    if call.data == 'yes':
        bot.send_message(chat_id, information_received_lang[lang])
        bot.send_message(canal_id, f"{confirm_lang[lang]} {name}\n"
                                  f"{quest_offer_lang[lang]}{quest}\n"
                                  f"{user_phone_number_lang[lang]} {phone}")
        time.sleep(3)
        bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))

        bot.register_next_step_handler(call.message, main_menu)

    elif call.data == "no":
        bot.send_message(chat_id, connect_line_text[lang], reply_markup=generate_connect(lang))
        bot.register_next_step_handler(call.message, connect)


def social_media(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text == back_lang[lang]:
        return back(message)

def back_connect(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    if message.text == back_lang[lang]:
        bot.send_message(chat_id, connect_line_text[lang], reply_markup=generate_connect(lang))
        bot.register_next_step_handler(message, connect)


def back(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    if message.text == back_lang[lang]:
        bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))

        bot.register_next_step_handler(message, main_menu)


def news(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")
    bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))

    bot.register_next_step_handler(message, main_menu)

#########################################
#Musobaqa
#########################################

def send_answer_tournament(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "uz")

    username = message.from_user.username
    bot.send_message(chat_id, accept_answer_lang[lang])
    bot.send_message(group_id, f"Savol @{username}:\n\n{message.text}")
    time.sleep(2)
    bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))
    bot.register_next_step_handler(message, main_menu)

#########################################
#inline
#########################################

@bot.callback_query_handler(func=lambda call: call.data == "siyrat")
def siyrat_inline(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")

    bot.send_message(chat_id, question_lang[lang])
    bot.register_next_step_handler(call.message, send_answer_tournament)

@bot.callback_query_handler(func=lambda call: call.data == "_back")
def back_inline(call):
    chat_id = call.message.chat.id
    lang = user_langs.get(chat_id, "uz")
    bot.send_message(chat_id, choose_language[lang], reply_markup=generate_main_menu(lang))

    bot.register_next_step_handler(call.message, main_menu)

def send_status_update():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Hozirgi vaqtni olish
    message = f"*iTechAcademy* Bot is working. \n*Date & Time*: {current_time}"  # Xabarga vaqtni qo'shish
    bot.send_message(canal_id, message, parse_mode="Markdown")

send_status_update()
schedule.every(30).minutes.do(send_status_update)
schedule.every().hour.do(send_status_update)
schedule.every().day.at("10:30").do(send_status_update)

bot.polling(non_stop=True)

while True:
    schedule.run_pending()
    time.sleep(1)
