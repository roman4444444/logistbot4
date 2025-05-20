from flask import Flask, request
import telegram
import os

TOKEN = os.getenv("API_TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    bot.send_message(chat_id=chat_id, text="Принято!")
    return "ok"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    app.run()