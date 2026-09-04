import os, threading, time, telebot, google.generativeai as genai
from flask import Flask

BOT_TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GEMINI_KEY")

app = Flask(__name__)
@app.route('/')
def home(): return "Rafi Sarkar Bot Live!"

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()
time.sleep(1)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        print(f"Got message: {message.text}")
        bot.send_chat_action(message.chat.id, 'typing')
        r = model.generate_content(f"তুমি Rafi Sarkar Super Bot, সব উত্তর বাংলায় ছোট করে দাও। প্রশ্ন: {message.text}")
        bot.reply_to(message, r.text)
    except Exception as e:
        print(f"GEMINI ERROR: {e}")
        bot.reply_to(message, f"Error: {e}")

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    print(f"Checking keys - BOT: {bool(BOT_TOKEN)}, GEMINI: {bool(GEMINI_KEY)}")
    print("Starting Bot Polling...")
    bot.infinity_polling()
