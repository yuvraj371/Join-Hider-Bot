import os
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

MUST_JOIN = "MyOwnBots"

bot_token = os.environ.get("BOT_TOKEN", "")
api_hash = os.environ.get("API_HASH", "") 
api_id = os.environ.get("API_ID", "")
app = Client("Join-Hider-Bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  

@app.on_message(~filters.edited & filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:  # Not compulsory
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            try:
                await msg.reply(
                    f"please Please Join My Updates Channel To Use Me! And click on to Check /start !",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Join Updates Channel", url=link)]
                    ])
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")

@app.on_message(filters.group & (filters.service | filters.status_update))
async def hide_join_leave(client, message):
    if message.new_chat_members or message.left_chat_member:
        await message.delete()

@app.on_message(filters.command("start", "about", "help") & filters.private & ~filters.service)
async def reply_hello(client, message):
    mention = message.from_user.mention
    await message.reply(f"Hello {mention}, I'm a Join Hider Bot That Hides The Messages Like 'User joined' 'User left'. 👋")

app.run()
