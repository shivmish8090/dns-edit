# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

import logging
import telebot
from datetime import datetime
from config import LOGGER_GROUP_ID, BOT_TOKEN
from telebot import types 

bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(chat_id, message, photo=None):
    """Send log messages or photos to the specified chat."""
    try:
        if photo:
            bot.send_photo(chat_id=chat_id, photo=photo, caption=message, parse_mode="Markdown")
        else:
            bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    except Exception as e:
        logging.error(f"[log_message] Error sending log message: {e}")

def get_photo_id(photo_object):
    """Fetch file ID from a photo object."""
    try:
        return photo_object.big_file_id if photo_object else None
    except AttributeError:
        return None

def log_user_activity(user_id, username=None, first_name=None):
    """Log user activity with profile photo and details."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_profile_photos = bot.get_user_profile_photos(user_id)
    profile_photo = get_photo_id(user_profile_photos.photos[0][0]) if user_profile_photos.total_count > 0 else None
    
    mention = f"[{first_name}](tg://user?id={user_id})" if first_name else f"[User](tg://user?id={user_id})"
    username_display = f"@{username}" if username else "Not Set"

    message = (
        f"✨ *User Activity Log*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *User ID:* `{user_id}`\n"
        f"🙋 *Name:* {mention}\n"
        f"🔗 *Username:* {username_display}\n"
        f"🔄 *Action:* Started the bot\n"
        f"⏰ *Time:* `{current_time}`\n"
        f"📡 *Bot Status:* Active\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💎 _Welcome to our bot!_\n"
    )

    log_message(LOGGER_GROUP_ID, message, photo=profile_photo)

def log_group_activity(group_id, group_title, action):
    """Log group activity with group photo and details."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    group_photo = None

    try:
        chat = bot.get_chat(group_id)
        group_photo = get_photo_id(chat.photo)
    except Exception as e:
        logging.error(f"[log_group_activity] Error fetching group photo: {e}")

    action_emoji = "➕" if action.lower() == "added" else "➖"
    message = (
        f"✨ *Group Activity Log*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👥 *Group ID:* `{group_id}`\n"
        f"🏷️ *Group Name:* {group_title}\n"
        f"{action_emoji} *Action:* {action.capitalize()}\n"
        f"⏰ *Time:* `{current_time}`\n"
        f"📡 *Bot Status:* Active\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🌟 _Your group is now connected!_\n"
    )

    log_message(LOGGER_GROUP_ID, message, photo=group_photo)

def send_thank_you_message(user, group_name, group_id):
    """Send a stylish thank-you message with a link button to the group."""
    thank_you_message = f"""
**🤖 Thanks for adding me to the group {group_name}! 🤖**

I’m here to make your group safer and more efficient!  
Tap the button below to explore my features.

**🌟 Features:**
- Auto Delete Edit Messages
- Auto Delete Edit Media
- Group Security & Monitoring

🚀 Let’s make this group awesome together!  
Need help? Just ask! 💬
"""

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Plzz Click Me", url="https://t.me/EditGuardiansBot?start=start")
    markup.add(button)

    try:
        bot.send_message(group_id, thank_you_message, parse_mode="Markdown", reply_markup=markup)
        logging.info(f"Sent thank-you message to group {group_name} for adding the bot.")
    except Exception as e:
        logging.error(f"Error sending thank-you message to group {group_name}: {e}")