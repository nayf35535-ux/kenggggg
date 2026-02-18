import discord
from groq import Groq
import os

# الإعدادات الأساسية
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# الرقم الذي وضعته أنت
OFFICIAL_CHANNEL_ID = 1473781070783713320  

client_ai = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم التحديث! البوت {client.user} يعمل الآن في الروم المحدد فقط.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # التحقق من الروم المحدد أو الخاص (DM)
    if message.channel.id != OFFICIAL_CHANNEL_ID and not isinstance(message.channel, discord.DMChannel):
        return

    # الرد الخاص بالسؤال عن الهوية
    content_lower = message.content.lower()
    if "من انت" in content_lower or "من أنت" in content_lower or "who are you" in content_lower:
        await message.reply("أنا بوت ذكاء اصطناعي متطور، أعمل بتقنيات مشابهة لـ ChatGPT و Gemini، صُممت لمساعدتك في البرمجة والإجابة على تساؤلاتك بدقة وسرعة.")
        return

    # بداية معالجة الذكاء الاصطناعي
    async with message.channel.typing():
        try:
            chat_completion = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "أنت مساعد ذكاء اصطناعي متطور (مثل ChatGPT و Gemini). يجب أن تجيب دائماً باللغة العربية فقط وبشكل طبيعي. ممنوع استخدام أي لغات أخرى إلا في حالة كتابة الأكواد البرمجية."
                    },
                    {"role": "user", "content": message.content}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2048,
            )
            
            response = chat_completion.choices[0].message.content
            if response:
                await message.reply(response)
                
        except Exception as e:
            print(f"Error: {e}")
            await message.reply("واجهت مشكلة بسيطة في معالجة طلبك، جرب مرة أخرى.")

client.run(TOKEN)
