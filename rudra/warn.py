# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_solution_button():
    """
    Creates an inline keyboard with the "Solution" button.
    """
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("🚀 Solution", url="https://t.me/EditGuardiansBot?start=start")
    keyboard.add(button)
    return keyboard

def warn_user(bot, message):
    """
    Warns the user for sending an edited message.
    """
    user = message.from_user
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(
            message.chat.id,
            f"⚠️ <b>{user.first_name}</b>, your message was deleted because it contained an <b>edited message</b>.",
            parse_mode="HTML",
            reply_markup=create_solution_button()
        )
    except Exception as e:
        print(f"Error deleting message: {e}")