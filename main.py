
import os
import telebot
from flask import Flask, request, abort

TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"].rstrip("/")
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "🔥 Welcome To FLEXYMODZ BOT!")

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(message, "✅ Bot is Working!")

@app.route("/")
def home():
    return "FLEXYMODZ Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token"
    ) != WEBHOOK_SECRET:
        abort(403)

    update = telebot.types.Update.de_json(
        request.get_data().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

bot.remove_webhook()
bot.set_webhook(
    url=f"{WEBHOOK_URL}/webhook",
    secret_token=WEBHOOK_SECRET
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
