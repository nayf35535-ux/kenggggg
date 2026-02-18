import discord
from groq import Groq
import os

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OFFICIAL_CHANNEL_ID = 1473781070783713320

if not TOKEN or not GROQ_API_KEY:
    raise ValueError("❌ تأكد من وضع التوكنات في Environment Variables")

client_ai = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def send_long_message(channel, content, reply_to=None):
    """تقسيم الرسائل الطويلة"""
    chunks = [content[i:i+1900] for i in range(0, len(content), 1900)]
    for chunk in chunks:
        if reply_to:
            await reply_to.reply(chunk)
            reply_to = None
        else:
            await channel.send(chunk)


@client.event
async def on_ready():
    print(f"✅ البوت {client.user} يعمل الآن في الروم المحدد.")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # السماح فقط بالروم المحدد أو الخاص
    if message.channel.id != OFFICIAL_CHANNEL_ID and not isinstance(message.channel, discord.DMChannel):
        return

    content_lower = message.content.lower()

    # سؤال الهوية
    if "من انت" in content_lower or "من أنت" in content_lower or "who are you" in content_lower:
        await message.reply(
            "أنا بوت ذكاء اصطناعي متطور، أعمل بتقنيات مشابهة لـ ChatGPT و Gemini، "
            "صُممت لمساعدتك في البرمجة والإجابة على تساؤلاتك بدقة وسرعة."
        )
        return

    async with message.channel.typing():
        try:
            chat_completion = client_ai.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "أنت مساعد ذكاء اصطناعي متطور. "
                            "أجب دائماً باللغة العربية بشكل طبيعي وواضح. "
                            "يسمح باستخدام الإنجليزية فقط داخل الأكواد البرمجية."
                        ),
                    },
                    {"role": "user", "content": message.content},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=2048,
            )

            response = chat_completion.choices[0].message.content

            if response:
                await send_long_message(message.channel, response, reply_to=message)

        except Exception as e:
            print(f"❌ Error: {e}")
            await message.reply("واجهت مشكلة بسيطة في معالجة طلبك، جرب مرة أخرى.")


client.run(TOKEN)
