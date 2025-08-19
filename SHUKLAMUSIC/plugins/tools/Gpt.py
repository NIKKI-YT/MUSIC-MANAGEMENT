import os
import requests
from SHUKLAMUSIC import app
from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters

# Load API key from environment variable (DON'T hardcode keys!)
API_KEY = os.getenv("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")

BASE_URL = "https://api.together.xyz/v1/chat/completions"

@app.on_message(
    filters.command(
        ["chatgpt", "ai", "ask", "gpt", "solve"],
        prefixes=["+", ".", "/", "-", "", "$", "#", "&"],
    )
)
async def chat_gpt(bot, message: Message):
    try:
        # Check if API key is missing
        if not API_KEY:
            await message.reply_text("❍ ᴇʀʀᴏʀ: API key not found. Please set TOGETHER_API_KEY in environment.")
            return

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "❍ ᴇxᴀᴍᴘʟᴇ:**\n\n/chatgpt ᴡʜᴏ ɪs - '𝐙 𝛆 ʀ 𝛂 ƚ 𝐡 𝚘 δ?"
            )
            return

        # Extract query
        query = message.text.split(' ', 1)[1]

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code != 200:
            await message.reply_text(
                f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}\n\n{response.text}"
            )
            return

        try:
            response_data = response.json()
        except ValueError:
            await message.reply_text("❍ ᴇʀʀᴏʀ: Invalid response format (not JSON).")
            return

        # Safely extract assistant reply
        result = None
        if "choices" in response_data and len(response_data["choices"]) > 0:
            if "message" in response_data["choices"][0]:
                result = response_data["choices"][0]["message"].get("content")
            elif "text" in response_data["choices"][0]:
                result = response_data["choices"][0]["text"]

        if result:
            await message.reply_text(
                f"{result.strip()} \n\nＡɴsᴡᴇʀᴇᴅ ʙʏ➛[-'𝐙 𝛆 ʀ 𝛂 ƚ 𝐡 𝚘 δ](https://t.me/CardioMuzicBot?start=_tgr_TzS1uiNkYWE9)",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("❍ ᴇʀʀᴏʀ: No valid response from API.")

    except Exception as e:
        await message.reply_text(f"**❍ ᴇʀʀᴏʀ: {e} **")
