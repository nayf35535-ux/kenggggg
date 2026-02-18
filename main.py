import discord
from groq import Groq
import os

# جلب المفاتيح
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# إعداد عميل Groq
client_ai = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)

@client_discord.event
async def on_ready():
    print(f'الحكيم الملحمي {client_discord.user} جاهز للرد باستخدام Groq!')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    async with message.channel.typing():
        try:
            # استخدام الموديل المحدث والمتاح حالياً
            chat_completion = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "أنت حكيم ملحمي تملك قوة النار والبرق، أجب باختصار وقوة."
                    },
                    {
                        "role": "user",
                        "content": message.content,
                    }
                ],
                model="llama-3.3-70b-versatile", 
            )
            
            response = chat_completion.choices[0].message.content
            await message.reply(response)
            
        except Exception as e:
            print(f"Error: {e}")
            await message.reply(f"واجهت مشكلة تقنية: {str(e)[:50]}")

client_discord.run(DISCORD_TOKEN)
