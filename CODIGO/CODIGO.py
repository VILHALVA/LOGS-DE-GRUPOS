import telebot
from telebot import types
import json
from CONFIG import TOKEN, ID_CANAL

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Olá! Sou um bot de logs de grupo.")

def log_message(log_text):
    bot.send_message(ID_CANAL, log_text, parse_mode='HTML')

@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    for new_member in message.new_chat_members:
        log_text = f"✅ <b>#ENTRADA</b>\n• Nome: {new_member.first_name} {new_member.last_name or ''} [{new_member.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
        log_message(log_text)

@bot.message_handler(content_types=['left_chat_member'])
def handle_left_member(message):
    left_member = message.left_chat_member
    log_text = f"✅ <b>#SAIDA</b>\n• Nome: {left_member.first_name} {left_member.last_name or ''} [{left_member.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
    log_message(log_text)

@bot.chat_member_handler()
def handle_chat_member_update(message):
    status = message.new_chat_member.status
    user = message.new_chat_member.user
    old_status = message.old_chat_member.status
    admin = message.from_user

    if status == 'kicked':
        log_text = f"🚷 <b>#BAN</b>\n• De: {admin.first_name} (http://t.me/{admin.username}) [{admin.id}]\n• Para: {user.first_name} [{user.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
        log_message(log_text)
    elif status == 'restricted' and old_status == 'member':
        log_text = f"🚷 <b>#MUTE</b>\n• De: {admin.first_name} (http://t.me/{admin.username}) [{admin.id}]\n• Para: {user.first_name} [{user.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
        log_message(log_text)
    elif status == 'left' and old_status == 'kicked':
        log_text = f"✅ <b>#UNBAN</b>\n• De: {admin.first_name} (http://t.me/{admin.username}) [{admin.id}]\n• Para: {user.first_name} [{user.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
        log_message(log_text)
    elif status == 'member' and old_status == 'restricted':
        log_text = f"✅ <b>#UNMUTE</b>\n• De: {admin.first_name} (http://t.me/{admin.username}) [{admin.id}]\n• Para: {user.first_name} [{user.id}]\n• Grupo: {message.chat.title} [{message.chat.id}]\n"
        log_message(log_text)

if __name__ == '__main__':
    print("Bot Iniciado!")
    bot.polling()
