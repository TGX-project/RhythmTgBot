from time import sleep
from pyrogram import Client
from pyrogram.types.messages_and_media import Message


async def info(bot:Client,msg:Message) :
    chat_id = msg.chat.id
    msg = await bot.send_message(chat_id,text="hi hello world")
    msg_id = msg.id 
    for x in range(0,10) :
        sleep(2)
        await bot.edit_message_text(chat_id=msg.chat.id,message_id=msg_id,text=f"hi {x}")
#    await bot.edit_message_text(chat_id=msg.chat.id,message_id=msg.id+1,text="hello")
