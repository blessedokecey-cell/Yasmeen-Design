import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# تفعيل الـ Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# جلب البيانات من متغيرات البيئة
TOKEN = os.getenv("BOT_TOKEN")
WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")
DEV_VIDEO = os.getenv("DEV_VIDEO")
DEV_USER = os.getenv("DEVELOPER_USER")
TREND_CH = os.getenv("TREND_CHANNEL")
SUPPORT_CH = os.getenv("SUPPORT_CHANNEL")
YS_CH = os.getenv("YS_CHANNELS")

# دالة الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
    # تصميم الأزرار العصري والمتناسق هندسياً (2 في الصف الأول، 2 في الثاني، وزر ريتاج المميز في الأسفل)
    keyboard = [
        [
            InlineKeyboardButton("📜 Y.S", callback_data="ys_list"),
            InlineKeyboardButton("🏆 تـرنـد²⁰²⁷", callback_data="trend_info")
        ],
        [
            InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_info"),
            InlineKeyboardButton("🛠️ الدعم", callback_data="support_info")
        ],
        [
            # زر ريتاج ينقل المستخدم مباشرة إلى البوت الآخر عند الضغط عليه
            InlineKeyboardButton("👑 ريتاج", url="https://t.me")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال فيديو الترحيب وتحته الأزرار الخمسة مباشرة
    await update.message.reply_video(
        video=WELCOME_VIDEO,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# دالة التحكم بالضغطات
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ys_list":
        # تقسيم قائمة القنوات وعرضها مرقمة بالترتيب
        channels = [ch.strip() for ch in YS_CH.split(",")]
        ys_text = "📜 **قائمة القنوات التابعة لنا بالترتيب:**\n\n"
        for index, ch in enumerate(channels, start=1):
            ys_text += f"{index}. {ch}\n"
        await query.message.reply_text(text=ys_text, parse_mode="Markdown")
        
    elif query.data == "trend_info":
        trend_text = (
            "🏆 **قناة تـرنـد²⁰²⁷ للمسابقات والجوائز**\n\n"
            f"تابع القناة الرسمية لتكون أول المشاركين والفائزين بالعروض الحصرية:\n👉 {TREND_CH}"
        )
        await query.message.reply_text(text=trend_text, parse_mode="Markdown")
        
    elif query.data == "dev_info":
        dev_text = (
            "👨‍💻 **البطاقة التعريفية لمطور البوت**\n\n"
            f"للتواصل، الاستفسار، أو طلب تطوير بوتات خاصة، يمكنك مراسلة المطور عبر حسابه:\n👉 {DEV_USER}"
        )
        # إرسال فيديو هوية المطور مع النص
        await query.message.reply_video(
            video=DEV_VIDEO,
            caption=dev_text,
            parse_mode="Markdown"
        )
        
    elif query.data == "support_info":
        support_text = (
            "🛠️ **قسم الدعم الفني والمساعدة**\n\n"
            f"إذا واجهتك أي مشكلة أو كان لديك اقتراح، تفضل بزيارة قناة الدعم:\n👉 {SUPPORT_CH}"
        )
        await query.message.reply_text(text=support_text, parse_mode="Markdown")

def main():
    # بناء التطبيق باستخدام التوكن من متغيرات البيئة
    application = Application.builder().token(TOKEN).build()
    
    # تسجيل الأوامر والضغطات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("البوت ياسمين جاهز ويعمل الآن بنظام 5 أزرار عصرية...")
    
    # التعديل هنا: استخدام دالة التحديث النظيف لمنع تعليق السيرفر
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()

  
