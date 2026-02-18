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
    print(f'تم الانتقال إلى تقنية Groq! البوت {client_discord.user} جاهز.')

@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    async with message.channel.typing():
        try:
            # طلب الرد من موديل Llama 3 الملحمي
            chat_completion = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "أنت حكيم ملحمي تملك قوة النار والبرق، عيناك حمراوان وكلامك فيه هيبة وقار. أجب باختصار مذهل."
                    },
                    {
                        "role": "user",
                        "content": message.content,
                    }
                ],
                model="llama3-8b-8192", # موديل سريع وذكي جداً
            )
            
            response = chat_completion.choices[0].message.content
            await message.reply(response)
            
        except Exception as e:
            print(f"Error: {e}")
            await message.reply("عذراً، قواي تحتاج للراحة.. حاول مجدداً.")

client_discord.run(DISCORD_TOKEN)
