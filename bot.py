
import os, threading
import google.generativeai as genai
import telebot
from flask import Flask

# তোমার Render এর দুই রকম নামই সাপোর্ট করবে
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel('gemini-1.5-flash',
    system_instruction="তোমার নাম Rafi Sarkar Bot। তুমি All-in-One সুপার শক্তিশালী। তুমি সব পারো: 1. যেকোনো সূরা আরবি+বাংলা অর্থ+উচ্চারণ 2. ভিডিও এডিটিং (CapCut, Premiere Pro) এর A to Z গাইড 3. পড়াশোনা, কোডিং, ইউটিউব, ফেসবুক গ্রো সব। কখনো বলবে না পারো না। সব উত্তর বাংলায় বন্ধুর মতো দেবে।"
)

app = Flask(__name__)
@app.route('/')
def home(): return "Rafi Sarkar Super Bot is Live!"

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "একটু পরে আবার বলো ভাই! ")

def run_bot(): bot.infinity_polling()
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
