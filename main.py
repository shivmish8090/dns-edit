# Copyright (c) 2025 Rajputshivsingh65. All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
# Written by Rajputshivsingh65 <choudharydilip256@gmail.com>, January 2025.
import os
import logging 
from telethon import TelegramClient, events, Button
from motor.motor_asyncio import AsyncIOMotorClient

from rudra.start import send_start_message
from rudra.delete_media_edits import handle_media_edited_message
from rudra.user import get_group_count, get_user_count, add_group, add_user
from rudra.warn import warn_user
from rudra.broadcast import send_broadcast_message
from rudra.logging import log_user_activity, log_group_activity, send_thank_you_message 

from rudra.delete_edits import handle_edited_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_NAME = os.getenv("DB_NAME", "edit")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URL")
OWNER_ID = int(os.getenv("OWNER_ID"))
LOGGER_GROUP_ID = int(os.getenv("LOGGER_GROUP_ID"))

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

bot = TelegramClient('anon', API_ID, API_HASH)

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.editguardian
users_collection = db["users"]
groups_collection = db["groups"]

async def add_user(user_id):
    if not await users_collection.find_one({"user_id": user_id}):
        await users_collection.insert_one({"user_id": user_id})

async def add_group(group_id):
    if not await groups_collection.find_one({"group_id": group_id}):
        await groups_collection.insert_one({"group_id": group_id}) 

async def remove_group(group_id):
    if await groups_collection.find_one({"group_id": group_id}):
        await groups_collection.delete_one({"group_id": group_id})

async def get_all_users():
    users = []
    async for user in users_collection.find():
        try:
            users.append(user["user_id"])
        except Exception:
            pass
    return users
    
async def get_all_groups():
    group = []
    async for chat in groups_collection.find():
        try:
            group.append(chat["group_id"])
        except Exception:
            pass
    return users    

async def main():
    await bot.start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(func = lambda e: e.text.startswith("/start") and e.is_private, incoming=True))
async def handle_start(event):
    await add_user(user_id)
    user_id = event.sender_id
    user = await event.get_sender()
    photo = None
    async for p in bot.iter_profile_photos(user, limit=1):
        photo = await bot.download_media(p)
        break
        
    mention = f"[{user.first_name}](tg://user?id={user.id})"
    message = (
        f"✨ *User Activity Log*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *User ID:* `{user_id}`\n"
        f"🙋 *Name:* {mention}\n"
        f"🔗 *Username:* {user.username if user.username else 'No User name'}\n"
        f"🔄 *Action:* Started the bot\n"
        f"⏰ *Time:* `{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`\n"
        f"📡 *Bot Status:* Active\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"💎 _Welcome to our bot!_\n"
    )
    await tbot.send_message(LOGGER_GROUP_ID, message, file=photo)

    start_text = (
        f"Hello {mention} 👋, I'm your 𝗘𝗱𝗶𝘁 𝗚𝘂𝗮𝗿𝗱𝗶𝗮𝗻 𝗕𝗼𝘁, here to maintain a secure environment for our discussions.\n\n"
        "🚫 𝗘𝗱𝗶𝘁𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗗𝗲𝗹𝗲𝘁𝗶𝗼𝗻: 𝗜'𝗹𝗹 𝗿𝗲𝗺𝗼𝘃𝗲 𝗲𝗱𝗶𝘁𝗲𝗱 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝘁𝗼 𝗺𝗮𝗶𝗻𝘁𝗮𝗶𝗻 𝘁𝗿𝗮𝗻𝘀𝗽𝗮𝗿𝗲𝗻𝗰𝘆.\n\n"
        "📣 𝗡𝗼𝘁𝗶𝗳𝗶𝗰𝗮𝗻𝗰𝗲𝘀: 𝗬𝗼𝘂'𝗹𝗹 𝗯𝗲 𝗶𝗻𝗳𝗼𝗿𝗺𝗲𝗱 𝗲𝗮𝗰𝗵 𝘁𝗶𝗺𝗲 𝗮 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝗶𝘀 𝗱𝗲𝗹𝗲𝘁𝗲𝗱.\n\n"
        "🌟 𝗚𝗲𝘁 𝗦𝘁𝗮𝗿𝘁𝗲𝗱:\n"
        "1. Add me to your group.\n"
        "2. I'll start protecting instantly.\n\n"
        "➡️ Click on 𝗔𝗱𝗱 𝗚𝗿𝗼𝘂𝗽 to add me and keep our group safe!"
    )
    buttons = [
    [Button.url("Update Channel", "https://t.me/Dns_Official_Channel"),
     Button.url("Update Group", "https://t.me/DNS_NETWORK")],
    [Button.url("Add Group", "https://t.me/EditGuardiansBot?start=start")]
    ]
    await event.respond(start_text, buttons=buttons

@bot.on(
    events.MessageEdited(func=lambda e.is_group, incoming=True)
)                        
async def on_message_edited(event):
    try:
        await event.delete()
        reason = "ᴇᴅɪᴛɪɴɢ ᴍᴇꜱꜱᴀɢᴇꜱ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ ʜᴇʀᴇ."

        if event.text:
            reason = "ᴇᴅɪᴛɪɴɢ ᴀ ᴍᴇꜱꜱᴀɢᴇ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
        elif message.photo:
            reason = "ʀᴇᴘʟᴀᴄɪɴɢ ᴏʀ ᴇᴅɪᴛɪɴɢ ᴀ ᴘʜᴏᴛᴏ ɪꜱ ɴᴏᴛ ᴘᴇʀᴍɪᴛᴛᴇᴅ."
        elif message.video:
            reason = "ʀᴇᴘʟᴀᴄɪɴɢ ᴏʀ ᴇᴅɪᴛɪɴɢ ᴀ ᴠɪᴅᴇᴏ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
        elif message.document:
            reason = "ʀᴇᴘʟᴀᴄɪɴɢ ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ ɪꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ."
        elif message.audio:
            reason = "ʀᴇᴘʟᴀᴄɪɴɢ ᴀ ᴀᴜᴅɪᴏ ꜰɪʟᴇ ɪꜱ ɴᴏᴛ ᴘᴇʀᴍɪᴛᴛᴇᴅ."
        elif message.video_note:
            reason = "ᴄʜᴀɴɢɪɴɢ ᴀ ᴠɪᴅᴇᴏ ɴᴏᴛᴇ ɪꜱ ɴᴏᴛ ᴀʟʟᴏᴡᴇᴅ."
        elif message.voice:
            reason = "ᴇᴅɪᴛɪɴɢ ᴀ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ ɪꜱ ɴᴏᴛ ᴘᴇʀᴍɪᴛᴛᴇᴅ."
        elif message.sticker:
            reason = "ʀᴇᴘʟᴀᴄɪɴɢ ᴀ ꜱᴛɪᴄᴋᴇʀ ɪꜱ ɴᴏᴛ ᴘᴇʀᴍɪᴛᴛᴇᴅ."
        await event.respond(reason)
    except Exception:
        return

@bot.on(events.NewMessage(func = lambda e: e.text.startswith("/stats"), incoming=True))
async def handle_user_count(event):
    if event.sender_id == OWNER_ID:
        user_count = len(await get_all_users())
        group_count =  len(await get_all_groups())
        await event.reply(f"Total users: {user_count}\nTotal Groups: {group_count}")
    else:
        await event.reply("You are not authorized to use this command.")

@bot.on(events.NewMessage(func = lambda e: e.text.startswith("/broadcast") and e.sender_id == OWNER_ID, incoming=True))
async def handle_broadcast(message):
    chat_ids = await get_all_users() + await get_all_groups()
    if event.is_reply:
        rmsg = await event.get_reply_message()
        for chat in chat_ids:
            try:
                await rmsg.forward_to(chat)
            except Exception:
                pass
    elif len(event.text.split()) => 2:
        msg = event.text.replace("/broadcast", "")
        for chat in chat_ids:
            try:
                await bot.send_message(chat, msg, link_preview=False)
            except Exception:
                pass
    
    else:
        await event.reply("Provide a message or Reply to a message to broadcast it.")

@bot.my_chat_member_handler(func=lambda member: member.new_chat_member.status in ["member", "administrator"])
def handle_bot_added_to_group(event):
    try:
        chat = event.chat
        if chat.type in ["group", "supergroup"]:
            group_id = chat.id
            group_name = chat.title
            user = event.from_user
            add_group(group_id)
            log_group_activity(group_id, group_name, "added")
            send_thank_you_message(user, group_name, group_id)
            logging.info(f"Bot added to group: {group_name} (ID: {group_id})")
    except Exception as e:
        logging.error(f"Error handling bot added to group: {e}")    

if __name__ == "__main__":
    bot.infinity_polling()
