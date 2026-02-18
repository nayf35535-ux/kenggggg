import discord
import google.generativeai as genai
import os

# جلب المفاتيح
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد المكتبة القديمة المستقرة
genai.configure(api_key=API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'الحكيم {client.user} يحاول النهوض من جديد!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async with message.channel.typing():
        try:
            # استخدام موديل 1.5 flash بدون إضافات معقدة
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(message.content)
            
            if response.text:
                await message.reply(response.text)
        except Exception as e:
            error_msg = str(e)
            print(f"Full Error: {error_msg}")
            
            # إذا كان الخطأ بسبب الموقع الجغرافي
            if "location" in error_msg.lower():
                await message.reply("خطأ: سيرفر Railway موجود في منطقة لا تدعمها جوجل. يجب تغيير الـ Region في Railway.")
            elif "403" in error_msg:
                await message.reply("خطأ 403: المفتاح مرفوض. تأكد من تفعيل Gemini API في Google Cloud.")
            else:
                await message.reply(f"العائق هو: {error_msg[:100]}")

client.run(TOKEN)
