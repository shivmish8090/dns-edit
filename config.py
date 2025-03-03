# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.

import os
DB_NAME = os.getenv("DB_NAME", "edit")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URL")
OWNER_ID = os.getenv("OWNER_ID")
LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID"))