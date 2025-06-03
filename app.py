from flask import Flask, request
import openai
import telegram
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)  # 🔥 Обязательно!

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text")

        if text:
            # 🔥 Новый способ запроса к OpenAI
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты дружелюбный человек. Отвечай от его имени."},
                    {"role": "user", "content": text}
                ]
            )
            reply = response.choices[0].message.content
            bot.send_message(chat_id=chat_id, text=reply)

    return "ok"

@app.route("/", methods=["GET"])
def index():
    return "Telegram GPT bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
