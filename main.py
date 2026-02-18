import discord
from groq import Groq
import os

# الإعدادات الأساسية
TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
# ضع هنا ID الروم الذي تريده (يمكنك جلب الـ ID بضغط كليك يمين على الروم في ديسكورد ثم Copy ID)
OFFICIAL_CHANNEL_ID = 1473781070783713320  # استبدل هذا الرقم بـ ID الروم الخاص بك

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

    # التحقق مما إذا كانت الرسالة في الروم المحدد فقط
    # إذا أردت أن يعمل في كل الرومات، قم بإلغاء تفعيل هذا الشرط
    if message.channel.id != OFFICIAL_CHANNEL_ID and not isinstance(message.channel, discord.DMChannel):
        return

    # الرد الخاص بالسؤال عن الهوية
    content_lower = message.content.lower()
    if "من انت" in content_lower or "من أنت" in content_lower or "who are you" in content_lower:
        await message.reply("أنا بوت ذكاء اصطناعي متطور، أعمل بتقنيات مشابهة لـ ChatGPT و Gemini، صُممت لمساعدتك في البرمجة والإجابة على تساؤلاتك بدقة وسرعة.")
        return

    async with message.channel.typing():
        try:
            chat_completion = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "أنت مساعد ذكاء اصطناعي متطور مثل ChatGPT و Gemini. خبير في البرمجة والعلوم. أجب بأسلوب ذكي وواضح."
                    },
                    {"role": "user", "content": message.content}
                ],
                model="llama-3.3-70b-versatile",
            )
            
            response = chat_completion.choices[0].message.content
            await message.reply(response)
        except Exception as e:
            print(f"Error: {e}")
            await message.reply("واجهت مشكلة بسيطة، جرب مرة أخرى.")

client.run(TOKEN)
