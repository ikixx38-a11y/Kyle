import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

# Token ကို Environment Variable ကနေ ယူမယ်
TOKEN = os.getenv("8773647679:AAFSXJLs_x0mTnnI5U0xRytdk7MDvC3eV2A")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စာသား သို့မဟုတ် ပုံနဲ့တွဲပါတဲ့စာသားကို ယူမယ်
    text = update.message.text or update.message.caption
    if not text: return

    # အပေါင်း၊ အနှုတ်၊ အမြှောက်၊ အစား လက္ခဏာနဲ့ ဂဏန်းတွေကိုပဲ သန့်စင်ယူမယ်
    # Emoji နဲ့ တခြားစာသားတွေကို ဖယ်ထုတ်ပစ်တာပါ
    clean_text = text.replace('×', '*').replace('÷', '/')
    clean_text = re.sub(r'[^0-9+\-*/.]', '', clean_text)

    try:
        # တွက်ချက်မယ်
        result = eval(clean_text)
        # Mono format (`...`) နဲ့ ပြန်ပို့မယ်
        response = f"`{result}`"
        await update.message.reply_text(response, parse_mode='MarkdownV2')
    except:
        pass # မတွက်နိုင်တဲ့စာသားဆိုရင် ဘာမှပြန်မလုပ်ဘူး

if __name__ == '__main__':
    keep_alive() # Web server စမယ်
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.Caption, calculate))
    app.run_polling()
