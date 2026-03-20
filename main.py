import os
import re
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Render အတွက် Port setting
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# သင်္ချာတွက်ချက်မှု Logic
def calculate_expression(text):
    # Emoji နဲ့ စာသားတွေကို ဖယ်ထုတ်ပြီး ကိန်းဂဏန်းနဲ့ လက္ခဏာကိုပဲ ယူမယ်
    # × ကို * အဖြစ်၊ ÷ ကို / အဖြစ် ပြောင်းလဲပေးမယ်
    text = text.replace('×', '*').replace('÷', '/')
    clean_text = re.sub(r'[^\d+\-*/.]', '', text)
    
    try:
        if not clean_text:
            return None
        result = eval(clean_text)
        return result
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စာသားသီးသန့်ဖြစ်စေ၊ ပုံနဲ့တွဲထားတဲ့စာဖြစ်စေ ယူမယ်
    text = update.message.text or update.message.caption
    
    if text:
        result = calculate_expression(text)
        if result is not None:
            # Monoformat (`...`) နဲ့ ပြန်ပို့ပေးမယ်
            await update.message.reply_text(f"`{result}`", parse_mode='MarkdownV2')

if __name__ == '__main__':
    # Flask server ကို background မှာ run မယ်
    keep_alive()
    
    # Telegram Bot Token ကို Render ရဲ့ Environment Variable မှာ ထည့်ပေးပါ
    TOKEN = os.environ.get('8795033266:AAEgEL-R7WZ0APY33BhFJcv2OFtyHGuqFMY')
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Message တွေအကုန်လုံး (စာရော ပုံရော) ကို လက်ခံမယ်
    msg_handler = MessageHandler(filters.TEXT | filters.CAPTION, handle_message)
    application.add_handler(msg_handler)
    
    application.run_polling()
