import discord
import google.generativeai as genai
import os

# قراءة التوكنات
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد ذكاء Gemini
genai.configure(api_key=GEMINI_API_KEY)

# تغيير الموديل هنا إلى الإصدار الأحدث 1.5
model = genai.GenerativeModel('gemini-1.5-flash')

# إعدادات ديسكورد
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تحديث البوت! هو الآن يعمل بنموذج Gemini 1.5 Flash باسم: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async with message.channel.typing():
        try:
            # صياغة الطلب
            prompt = f"أنت حكيم ملحمي تملك قوة النار والبرق، عيناك حمراوان وكلامك فيه هيبة وقار. أجب باختصار على: {message.content}"
            
            # طلب الرد من الموديل الجديد
            response = model.generate_content(prompt)
            
            await message.reply(response.text)
        except Exception as e:
            print(f"حدث خطأ: {e}")
            await message.reply("عذراً، واجهت مشكلة في التفكير.. حاول مرة أخرى.")

client.run(DISCORD_TOKEN)
