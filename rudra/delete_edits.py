# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

import time

def handle_edited_message(bot, message):
    original_time = message.date
    current_time = int(time.time())
    time_diff = current_time - original_time

    if time_diff > 0:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")