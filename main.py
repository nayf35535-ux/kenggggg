import discord
from google import genai
import os
import asyncio

# جلب المفاتيح
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد العميل الجديد
client_ai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'الحكيم الملحمي {client_discord.user} عاد من جديد!')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    async with message.channel.typing():
        try:
            # استخدام الطريقة الجديدة للمكتبة المحدثة
            response = client_ai.models.generate_content(
                model="gemini-1.5-flash", 
                contents=f"أنت حكيم ملحمي بقوة النار والبرق، أجب باختصار: {message.content}"
            )
            
            await message.reply(response.text)
        except Exception as e:
            print(f"ERROR DETAILS: {e}")
            await message.reply(f"لا زال الظلام يحيط بي.. الخطأ: {str(e)[:50]}")

client_discord.run(DISCORD_TOKEN)
