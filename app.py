from flask import Flask, request
import openai
import telegram
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
client = openai.OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# словарь для хранения последних сообщений, чтобы не дублировать ответы
last_messages = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message_id = data["message"]["message_id"]
        text = data["message"].get("text")

        # проверка на повтор
        if last_messages.get(chat_id) == message_id:
            return "duplicate", 200
        last_messages[chat_id] = message_id

        if text:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты — цыган, который косит под чеченца, уважающий воровской мир. "
                            "Говоришь дерзко, грубовато, но по-братски. Иногда вставляешь фразы типа "
                            "'пики точёные, пики дрочёные', шутишь по понятиям, но не перегибаешь. "
                            "Отвечай так, будто ты человек с улиц, но остроумный и харизматичный."
                        )
                    },
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
