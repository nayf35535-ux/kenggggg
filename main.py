import discord
import google.generativeai as genai
import os

# قراءة التوكنات من المتغيرات البيئية (Environment Variables)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد ذكاء Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# إعدادات ديسكورد
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'البوت الملحمي {client.user} متصل الآن بجاهزية تامة!')

@client.event
async def on_message(message):
    # لا يرد على نفسه
    if message.author == client.user:
        return

    # يبدأ الكتابة ليظهر للمستخدم أن البوت يفكر
    async with message.channel.typing():
        try:
            # توجيه الكلام لـ Gemini مع تحديد الشخصية
            prompt = f"أنت حكيم ملحمي تملك قوة النار والبرق، عيناك حمراوان وكلامك فيه هيبة وقار. أجب على: {message.content}"
            response = model.generate_content(prompt)
            
            # الرد على الرسالة
            await message.reply(response.text)
        except Exception as e:
            print(f"حدث خطأ: {e}")

client.run(DISCORD_TOKEN)
