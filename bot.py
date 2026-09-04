import os
import threading
import telebot
import google.generativeai as genai
from flask import Flask

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")

print(f"Checking keys - BOT: {bool(BOT_TOKEN)}, GEMINI: {bool(GEMINI_KEY)}")

app = Flask(__name__)
@app.route('/')
def home():
    return "Rafi Sarkar Super Bot is Live!"

bot = telebot.TeleBot(BOT_TOKEN)

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    try:
        if not model:
            bot.reply_to(message, "Gemini Key পাওয়া যায়নি ভাই, Render এ চেক করো")
            return
        bot.send_chat_action(message.chat.id, 'typing')
        prompt = f"তুমি Rafi Sarkar Super Bot, সব প্রশ্নের উত্তর বাংলায় দাও। ইউজারের প্রশ্ন: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "একটু পরে আবার বলো ভাই!")

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Starting Bot Polling...")
    bot.infinity_polling()
