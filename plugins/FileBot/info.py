import os
import telegraminfo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message((filters.private | filters.group) & filters.command(["info", "information"]))
async def info(bot, update):
    if (not update.reply_to_message) and ((not update.forward_from) or (not update.forward_from_chat)):
        info = telegraminfo.user(update.from_user)
    elif update.reply_to_message and update.reply_to_message.forward_from:
        info = telegraminfo.user(update.reply_to_message.forward_from)
    elif update.reply_to_message and update.reply_to_message.forward_from_chat:
        info = telegraminfo.chat(update.reply_to_message.forward_from_chat)
    elif (update.reply_to_message and update.reply_to_message.from_user) and (not update.forward_from or not update.forward_from_chat):
        info = telegraminfo.user(update.reply_to_message.from_user)
    else:
        return
    try:
        await update.reply_text(
            text=info+"\n\nMade by @subhan011",
            reply_markup=BUTTONS,
            disable_web_page_preview=True,
            quote=True
        )
    except Exception as error:
        await update.reply_text(error)
