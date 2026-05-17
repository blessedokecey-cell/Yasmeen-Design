import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تفعيل تسجيل الأخطاء البرمجية
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# قراءة التوكن ومتغير الفيديو من Railway
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")

# دالة الترحيب الأساسية عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
    # [التعديل الجذري والنهائي] أزرار روابط مباشرة مدمجة ومحمية تنتقل فوراً داخل التطبيق
    keyboard = [
        [
            # زر Y.S يفتح القنوات مباشرة للمستخدم عبر رابط تليجرام الداخلي
            InlineKeyboardButton("📜 Y.S", url="https://t.me"),
            InlineKeyboardButton("🏆 تـرنـد²⁰²٧", url="https://t.me")
        ],
        [
            InlineKeyboardButton("👨‍💻 المطور", url="https://t.me"),
            InlineKeyboardButton("🛠️ الدعم", url="https://t.me")
        ],
        [
            InlineKeyboardButton("👑 ريتاج", url="https://t.me")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_video(
        video=WELCOME_VIDEO,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    if not TOKEN:
        print("❌ خطأ: التوكن مفقود في لوحة تحكم المتغيرات بـ Railway!")
        return

    # بناء وتشغيل البوت بنظام استقبال الأوامر الصريح
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("🚀 البوت ياسمين يعمل الآن بنظام التوجيه الفوري المستقر...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
    
