import telebot
import random
import time
from telebot import types

TOKEN = '5729763018:AAFqRQGtJswTek3py-OxMg-QYniSJwDpXsQ'

bot = telebot.TeleBot(TOKEN)

members = dict()
banned_members = dict()

start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
item_1 = types.KeyboardButton("Make new BOSS")  # Сделать кого-то в чате админом
item_2 = types.KeyboardButton("Punish / Pardon")  # Забанить/разбанить человека в чате
item_3 = types.KeyboardButton("Dungeon statistics")  # Достать статистику по чату: сколько людей, сколько админов
item_4 = types.KeyboardButton("You've got the wrong door")  # Заставить бота самого уйти из чата
start_markup.add(item_1, item_2, item_3, item_4)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, "I woke up boss. What is your command?",
                     reply_markup=start_markup)
    bot.set_chat_title(message.chat.id, "Dungeon")  # новое название
@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    for member in message.new_chat_members:
        members[member.username] = member.id
        bot.send_message(message.chat.id, "Welcome to the club, " + member.username + '!')


@bot.message_handler(content_types=['text', 'emoji'])
def message_reply(message):
    if message.text == "Make new BOSS":
        if members:
            bot.send_dice(message.chat.id)
            time.sleep(3)
            lucky_member = random.choice(list(members.keys()))
            bot.promote_chat_member(message.chat.id, members[lucky_member])
            bot.send_message(chat_id=message.chat.id, text="Now " + lucky_member + " is an admin. Lucky!")
            bot.send_message(message.chat.id, "What's next?", reply_markup=start_markup)
        else:
            bot.send_message(chat_id=message.chat.id, text="You are alone, bro")
        bot.send_message(message.chat.id, "What's next?", reply_markup=start_markup)

    elif message.text == "Punish / Pardon":
        markup = types.ReplyKeyboardMarkup()
        item_5 = types.KeyboardButton("Punish")
        item_6 = types.KeyboardButton("Pardon")
        markup.add(item_5, item_6)
        bot.send_message(message.chat.id, "what to do with the fate of a random member?", reply_markup=markup)

    elif message.text == 'Dungeon statistics':
        admins_qty = str(len(bot.get_chat_administrators(message.chat.id)))
        members_qty = str(bot.get_chat_member_count(message.chat.id))
        bot.send_message(message.chat.id, "All members:" + members_qty + '\n' + "Administrators: " + admins_qty)
        bot.send_message(message.chat.id, "What's next?", reply_markup=start_markup)

    elif message.text == "You have got the wrong door":
        bot.send_message(message.chat.id, "See you space cowboys!")
        bot.leave_chat(message.chat.id)

    elif message.text == "Punish":
        if members:
            bot.send_dice(message.chat.id)
            time.sleep(3)
            lucky_member = random.choice(list(members.keys()))
            bot.ban_chat_member(message.chat.id, members[lucky_member])
            banned_members[lucky_member] = members[lucky_member]
            del members[lucky_member]
            bot.send_message(chat_id=message.chat.id, text="Sad for you, " + lucky_member)
        else:
            bot.send_message(chat_id=message.chat.id, text="There is no one to ban")
        bot.send_message(message.chat.id, "What's next?", reply_markup=start_markup)

    elif message.text == "Pardon":
        if banned_members:
            bot.send_dice(message.chat.id)
            time.sleep(3)
            lucky_member = random.choice(list(banned_members.keys()))
            bot.unban_chat_member(message.chat.id, banned_members[lucky_member])
            bot.send_message(chat_id=message.chat.id, text=lucky_member + " has been unbanned. Lucky!")
            members[lucky_member] = banned_members[lucky_member]
            del banned_members[lucky_member]
        else:
            bot.send_message(chat_id=message.chat.id, text="There is no one to unban")
        bot.send_message(message.chat.id, "What's next?", reply_markup=start_markup)


bot.polling(none_stop=True, interval=0)
