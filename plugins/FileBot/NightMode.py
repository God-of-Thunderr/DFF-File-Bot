from pyrogram import Client, filters
from os import environ
from pyrogram import Client, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from info import CHAT_ID, TIMEZONE

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

async def group_close():
    try:
        await Client.send_message(
                CHAT_ID,
                "It's 12:00 AM\nGroup is Closing!"
                )
        await Client.set_chat_permissions(
                CHAT_ID,
                ChatPermissions()
                )
    except BaseException as e:
        await Client.send_message(
                CHAT_ID,
                f"**Error while closing group:** `{e}`"
                )
        logging.error(str(e))

async def group_open():
    try:
        await Client.send_message(
                CHAT_ID,
                "It's 6:00 AM\nGroup is opening"
                )
        await Client.set_chat_permissions(
                CHAT_ID,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_stickers=True,
                    can_send_animations=True
                    )
                )
    except BaseException as e:
        logging.error(str(e))
        await Client.send_message(
                CHAT_ID,
                f"**Error while opening group:**\n`{e}`"
                )


@Client.on_message(filters.command("privatestrt"))
async def privatestrt(client, message):
    await message.reply(
            "Heya, I am a NightMode Bot\n**(c) [Reeshuxd](https://github.com/Reeshuxd)**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(" My Source Code", url="github.com/Reeshuxd/NightModeBot")]
                ]
            )
        )

scheduler = AsyncIOScheduler(timezone=TIMEZONE)
scheduler.add_job(group_close, trigger="cron", hour=11, minute=59)
scheduler.add_job(group_open, trigger="cron", hour=5, minute=59)
scheduler.start()



