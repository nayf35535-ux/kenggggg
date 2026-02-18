import discord
import google.generativeai as genai
import os

# جلب المفاتيح
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد Gemini وتجاهل فلاتر الأمان لتجنب الرفض
genai.configure(api_key=GEMINI_API_KEY)

# إعدادات لضمان عدم حظر الردود العادية
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    safety_settings=safety_settings
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'البوت الملحمي {client.user} جاهز للغزو!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async with message.channel.typing():
        try:
            # محاولة جلب الرد
            prompt = f"أنت حكيم ملحمي بقوة النار والبرق. أجب باختصار وهيبة: {message.content}"
            response = model.generate_content(prompt)
            
            if response.text:
                await message.reply(response.text)
            else:
                await message.reply("أعتذر، لم أستطع صياغة حكمة تليق بهذا السؤال.")
                
        except Exception as e:
            print(f"DEBUG ERROR: {e}") # هذا سيظهر لك السبب الحقيقي في Logs
            await message.reply(f"حدث خطأ فني: {str(e)[:100]}") # سيعطيك أول 100 حرف من الخطأ

client.run(DISCORD_TOKEN)
