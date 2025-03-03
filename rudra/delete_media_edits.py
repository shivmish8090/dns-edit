# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

def handle_media_edited_message(bot, message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error deleting media edit message: {e}")