import os
import telebot
from flask import Flask
from threading import Thread

# 1. Telegram Bot Token ကို Environment Variable ကနေ ဖတ်မယ်
TOKEN = os.getenv("8773647679:AAFAeUweMplswKY8NgwK0wsW8u8YHXqDVFk")
bot = telebot.TeleBot(TOKEN)

# 2. Render အတွက် Port Binding လုပ်ပေးဖို့ Flask Web Server တစ်ခု တည်ဆောက်မယ်
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    # Render က ပေးတဲ့ PORT (10000) မှာ run ပေးဖို့ ဖြစ်ပါတယ်
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Bot ရဲ့ လုပ်ဆောင်ချက်များ
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ဟလို! ကျွန်တော်က Render ပေါ်မှာ အောင်မြင်စွာ Run နေတဲ့ Bot ပါ။")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # သင်္ချာတွက်ချက်မှု လုပ်နိုင်အောင် ပြင်ဆင်ထားပေးပါတယ်
        result = eval(message.text)
        bot.reply_to(message, f"အဖြေမှာ - {result}")
    except:
        bot.reply_to(message, f"မင်း ပြောလိုက်တာက - {message.text}")

# 4. Flask ကို Thread နဲ့ နောက်ကွယ်မှာ run ပြီး Bot ကို အသက်သွင်းမယ်
def keep_alive():
    t = Thread(target=run_flask)
    t.start()

if __name__ == "__main__":
    print("Starting Bot...")
    keep_alive()  # Web Server ကို စတင်မယ်
    bot.infinity_polling()  # Bot ကို စတင်မယ်
