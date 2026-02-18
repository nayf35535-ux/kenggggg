import discord
from google import genai
import os

# المفاتيح
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد المكتبة مع إجبارها على استخدام الإصدار v1 المستقر
client_ai = genai.Client(
    api_key=API_KEY,
    http_options={'api_version': 'v1'} # هذه الإضافة هي المفتاح لكسر الـ 404
)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'تم تحديث المسار إلى v1! {client_discord.user} جاهز.')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    async with message.channel.typing():
        try:
            # طلب المحتوى
            response = client_ai.models.generate_content(
                model='gemini-1.5-flash',
                contents=message.content
            )
            await message.reply(response.text)
        except Exception as e:
            print(f"ERROR: {e}")
            await message.reply(f"لا زال هناك عائق.. النوع: {type(e).__name__}")

client_discord.run(TOKEN)
