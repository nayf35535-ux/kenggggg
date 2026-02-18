import discord
import google.generativeai as genai
import os

# جلب المفاتيح من Railway
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد Gemini
genai.configure(api_key=GEMINI_API_KEY)

# جربنا flash-latest لأنه الأكثر توافقاً
model = genai.GenerativeModel('gemini-1.5-flash-latest')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'البوت الملحمي {client.user} متصل ومستعد!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async with message.channel.typing():
        try:
            # إرسال السؤال لـ Gemini
            prompt = f"أنت حكيم ملحمي، أجب باختصار: {message.content}"
            response = model.generate_content(prompt)
            
            if response.text:
                await message.reply(response.text)
            else:
                await message.reply("توقفت قواي عن التفكير حالياً..")
                
        except Exception as e:
            # طباعة الخطأ في الـ Logs لمعرفته بدقة
            print(f"ERROR: {e}")
            # إذا فشل الموديل الأول، سنجرب الموديل الاحتياطي
            try:
                backup_model = genai.GenerativeModel('gemini-pro')
                res = backup_model.generate_content(message.content)
                await message.reply(res.text)
            except:
                await message.reply(f"لا زلت أواجه خطأ 404، تأكد من صلاحية الـ API Key.")

client.run(DISCORD_TOKEN)
