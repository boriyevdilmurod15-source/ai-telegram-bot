from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = "TOKEN"
OPENAI_API_KEY = "KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

users = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in users:
        users[user_id] = {"count": 0, "premium": False, "history": []}

    # limit
    if not users[user_id]["premium"]:
        if users[user_id]["count"] >= 5:
            await update.message.reply_text("❌ Limit tugadi. Premium oling.")
            return

    users[user_id]["count"] += 1
    users[user_id]["history"].append(text)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Sen foydali AI yordamchisan"},
            {"role": "user", "content": text}
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()