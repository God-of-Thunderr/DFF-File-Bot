import os
from plugins.filebot import tginfo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/Subhan011')]]
)


@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == "private":
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>First Name:</b> {first}\n<b>Last Name:</b> {last}\n<b>Username:</b> {username}\n<b>Telegram ID:</b> <code>{user_id}</code>\n<b>Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )

@Client.on_message(filters.private & filters.forwarded)
async def forwarded(bot, msg):
    if msg.forward_from:
        text = "Forward detected! \n\n"
        if msg.forward_from["is_bot"]:
            text += "**Bot**"
        else:
            text += "**User**"
        text += f'\n{msg.forward_from["first_name"]} \n'
        if msg.forward_from["username"]:
            text += f'@{msg.forward_from["username"]} \nID : `{msg.forward_from["id"]}`'
        else:
            text += f'ID : `{msg.forward_from["id"]}`'
        await msg.reply(text, quote=True)
    else:
        hidden = msg.forward_sender_name
        if hidden:
            await msg.reply(
                f"Forward detected but unfortunately, {hidden} has enabled forwarding privacy, so I can't get their id",
                quote=True,
            )
        else:
            text = f"Forward Detected. \n\n"
            if msg.forward_from_chat["type"] == "channel":
                text += "**Channel**"
            if msg.forward_from_chat["type"] == "supergroup":
                text += "**Group**"
            text += f'\n{msg.forward_from_chat["title"]} \n'
            if msg.forward_from_chat["username"]:
                text += f'@{msg.forward_from_chat["username"]} \n'
                text += f'ID : `{msg.forward_from_chat["id"]}`'
            else:
                text += f'ID : `{msg.forward_from_chat["id"]}`'
            await msg.reply(text, quote=True)

@Client.on_message((filters.private | filters.group) & filters.command(["info", "information"]))
async def info(bot, update):
    if (not update.reply_to_message) and ((not update.forward_from) or (not update.forward_from_chat)):
        info = tginfo.user(update.from_user)
    elif update.reply_to_message and update.reply_to_message.forward_from:
        info = tginfo.user(update.reply_to_message.forward_from)
    elif update.reply_to_message and update.reply_to_message.forward_from_chat:
        info = tginfo.chat(update.reply_to_message.forward_from_chat)
    elif (update.reply_to_message and update.reply_to_message.from_user) and (not update.forward_from or not update.forward_from_chat):
        info = tginfo.user(update.reply_to_message.from_user)
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

