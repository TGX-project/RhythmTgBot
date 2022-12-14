import os
import json
import time
import spotipy
from lib import config
from time import time
from pytube import YouTube
from pyrogram import Client
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram.types.messages_and_media import Message


credentials = SpotifyClientCredentials(client_id=config.CLIENT_ID,client_secret=config.SECRET)
sp = spotipy.Spotify(client_credentials_manager=credentials)


async def grab(bot:Client,msg:Message) :
    chat_id = msg.chat.id
    link = msg.text.replace("/grab ","")
    try :
        link_type = link.split("/")[3]
    except :
        await msg.reply_text("\"ɢʀᴀʙ\" doᥱs not sᥙρρort thιs sᥙffιx ⚠")
        return
    if link_type == "track" :
        message = await msg.reply("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ  ○○○")
        track = sp.track(link)["name"]
        print(track)
        await bot.edit_message_text(chat_id,message.id,text="ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ  ...")
        results = YoutubeSearch(track, max_results=1).to_dict()[0]["url_suffix"]
        link = YouTube(f"https://youtube.com{results}")
        video = link.streams.filter(only_audio=True).first()
        raw_file = video.download(output_path=".")
        base, ext = os.path.splitext(raw_file)
        await bot.edit_message_text(chat_id,message.id,text="sᴇɴᴅɪɴɢ ...")
        document = f"{base}.mp3"
        os.rename(raw_file,document)
        await msg.reply_document(document)
        await bot.delete_messages(chat_id,message.id)
        os.remove(document)
    elif link_type == "playlist" :
        offset = 0
        response = sp.playlist_items(link,offset=offset,fields='items.track.id,total',additional_types=['track'])
        x = time()
        completed = 0 
        message = await msg.reply_text(f"ᴘʟᴇᴀsᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ᴛʜɪs ᴡɪʟʟ ᴛᴀᴋᴇ ᴀ ᴡʜɪʟᴇ .\ncompleted : {completed}/{len(response['items'])}")

        for i in range(0,len(response["items"])):
            song_id = response["items"][i]["track"]["id"]
            track = sp.track(song_id)["name"]
            results = YoutubeSearch(track, max_results=1).to_dict()[0]["url_suffix"]
            link = YouTube(f"https://youtube.com{results}")
            video = link.streams.filter(only_audio=True).first()
            raw_file = video.download(output_path=".")
            base, ext = os.path.splitext(raw_file)
            document = f"{base}.mp3"
            os.rename(raw_file,document)
            await msg.reply_document(document,quote=False)
            completed += 1
            os.remove(document)
            await bot.edit_message_text(chat_id=chat_id,message_id=message.id,text=f"ᴘʟᴇᴀsᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ᴛʜɪs ᴡɪʟʟ ᴛᴀᴋᴇ ᴀ ᴡʜɪʟᴇ \n\ncoмpleтed : {completed}/{len(response['items'])}")
        y = time()
        z = y - x
        z = str(z).split(".")[0]
        await bot.delete_messages(chat_id,message_ids=message.id)
        await msg.reply_text(f"ᴛᴏᴛᴀʟ sᴏɴɢs : {len(response['items'])}\n\nᴛɪᴍᴇ ᴛᴏᴏᴋ : {z} sᥱᥴs")
    else :
        await msg.reply_text("oρᥱrᥲtιon not sᥙρρortᥱd ⚠")
