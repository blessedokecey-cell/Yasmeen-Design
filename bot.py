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
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # تم تحديثه ليتوافق مع Railway لديك
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
    
    # القائمة الرئيسية للأزرار
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

# دالة التحكم بالضغطات
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ys_list":
        # جلب القنوات وتقسيمها
        channels = [ch.strip() for ch in YS_CH.split(",")]
        
        # تحويل القنوات إلى أزرار تفاعلية تنقل المستخدم مباشرة عند الضغط عليها
        ys_buttons = []
        for ch in channels:
            # تنظيف اليوزر وتجهيز رابط تليجرام المباشر له t.me
            clean_ch = ch.replace("@", "")
            ys_buttons.append(InlineKeyboardButton(text=f"📢 {ch}", url=f"https://t.me{clean_ch}"))
        
        # ترتيب الأزرار في صفوف (كل سطر يحتوي على زرين ليكون المظهر منسقاً وعصرياً)
        ys_keyboard = [ys_buttons[i:i + 2] for i in range(0, len(ys_buttons), 2)]
        
        # إضافة زر للعودة للقائمة الرئيسية في نهاية قنوات Y.S (اختياري لراحة المستخدم)
        ys_keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")])
        
        ys_markup = InlineKeyboardMarkup(ys_keyboard)
        
        # إرسال رسالة الأزرار الجديدة
        await query.message.reply_text(
            text="📜 **قائمة القنوات التابعة لنا بالترتيب:**\nاضغط على أي زر للانتقال مباشرة إلى القناة:",
            reply_markup=ys_markup,
            parse_mode="Markdown"
        )
        
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

    elif query.data == "back_to_main":
        # حذف رسالة القنوات عند الضغط على زر العودة لتنظيف المحادثة
        await query.message.delete()

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("البوت ياسمين جاهز ويعمل الآن بنظام الأزرار العصري الشفاف...")
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
    
