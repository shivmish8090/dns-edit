# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

from rudra.user import get_all_users, get_all_groups
from config import LOGGER_GROUP_ID, BOT_TOKEN
from telebot import TeleBot

bot = TeleBot(BOT_TOKEN)

def send_broadcast_message(message_text):
    users = get_all_users()
    groups = get_all_groups()

    total_sent_users = 0
    total_failed_users = 0
    total_sent_groups = 0
    total_failed_groups = 0

    for user_id in users:
        try:
            bot.send_message(user_id, message_text)
            total_sent_users += 1
        except Exception:
            total_failed_users += 1

    for group_id in groups:
        try:
            bot.send_message(group_id, message_text)
            total_sent_groups += 1
        except Exception:
            total_failed_groups += 1

    try:
        result_message = (
            f"✨ <b>Broadcast Status</b> ✨\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👥 <b>Users:</b>\n"
            f"   🎯 <b>Total:</b> <u>{len(users)}</u>\n"
            f"   ✅ <b>Delivered:</b> <u>{total_sent_users}</u>\n"
            f"   ❌ <b>Failed:</b> <u>{total_failed_users}</u>\n\n"
            f"🛡 <b>Groups:</b>\n"
            f"   🎯 <b>Total:</b> <u>{len(groups)}</u>\n"
            f"   ✅ <b>Delivered:</b> <u>{total_sent_groups}</u>\n"
            f"   ❌ <b>Failed:</b> <u>{total_failed_groups}</u>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📝 <b>Message Sent:</b>\n"
            f"<code>{message_text}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📅 <b>Date & Time:</b> <i>{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i>"
        )
        bot.send_message(
            chat_id=LOGGER_GROUP_ID,
            text=result_message,
            parse_mode="HTML"
        )
        print("Broadcast summary logged successfully.")
    except Exception as e:
        print(f"Logging failed: {e}")