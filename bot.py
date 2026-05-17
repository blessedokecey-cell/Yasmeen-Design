import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تفعيل تسجيل الأخطاء البرمجية بدقة
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- [ إعدادات البيئة والتوكن ] ---
# ضع توكن البوت الحقيقي هنا مباشرة بين علامات التنصيص لضمان استقرار التشغيل للأبد
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ضع_توكن_البوت_هنا_إذا_تريد_وضعه_مباشرة")

# جلب باقي المتغيرات من Railway
WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")
DEV_VIDEO = os.getenv("DEV_VIDEO")
DEV_USER = os.getenv("DEVELOPER_USER", "@shaheen_ys") # قيمة افتراضية من قائمتك
TREND_CH = os.getenv("TREND_CHANNEL", "@fi1_oo")
SUPPORT_CH = os.getenv("SUPPORT_CHANNEL", "@shaheen_ys")
YS_CH = os.getenv("YS_CHANNELS", "")

# دالة الترحيب الأساسية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
    # تصميم لوحة الأزرار الرئيسية المتناسقة (2x2x1)
    keyboard = [
        [
            InlineKeyboardButton("📜 Y.S", callback_data="ys_list"),
            InlineKeyboardButton("🏆 تـرنـد²⁰²٧", callback_data="trend_info")
        ],
        [
            InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_info"),
            InlineKeyboardButton("🛠️ الدعم", callback_data="support_info")
        ],
        [
            # التعديل الاحترافي لفتح البوت الآخر داخلياً فوراً وبدون متصفح
            InlineKeyboardButton("👑 ريتاج", url="tg://resolve?domain=Ret_QueenBot")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال الفيديو والرسالة والأزرار مدمجة
    await update.message.reply_video(
        video=WELCOME_VIDEO,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# الدالة الذكية للتحكم بضغطات الأزرار التفاعلية (Callback Queries)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    # تفعيل الاستجابة الفورية لإنهاء حالة تعليق أو تحميل الزر
    await query.answer()

    if query.data == "ys_list":
        # فحص جلب قنوات YS وتنسيقها في أزرار شبكية
        if not YS_CH:
            await query.message.reply_text("⚠️ لم يتم إعداد قائمة القنوات في لوحة التحكم بعد.")
            return

        channels = [ch.strip() for ch in YS_CH.split(",") if ch.strip()]
        ys_buttons = []
        
        for ch in channels:
            clean_ch = ch.replace("@", "").strip()
            # استخدام الرابط الداخلي المباشر لفتح القنوات فوراً داخل التطبيق
            ys_buttons.append(InlineKeyboardButton(text=f"📢 {ch}", url=f"tg://resolve?domain={clean_ch}"))
        
        # توزيع الأزرار بشكل هندسي (زرين في كل صف)
        ys_keyboard = [ys_buttons[i:i + 2] for i in range(0, len(ys_buttons), 2)]
        # إضافة زر العودة الفخم في الأسفل
        ys_keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")])
        
        ys_markup = InlineKeyboardMarkup(ys_keyboard)
        
        await query.message.reply_text(
            text="📜 **قائمة القنوات التابعة لنا بالترتيب:**\nاضغط على أي قناة للانتقال إليها فوراً داخل التطبيق:",
            reply_markup=ys_markup,
            parse_mode="Markdown"
        )
        
    elif query.data == "trend_info":
        clean_trend = TREND_CH.replace("@", "").strip()
        trend_keyboard = [[InlineKeyboardButton("🚀 دخول القناة فوراً", url=f"tg://resolve?domain={clean_trend}")]]
        trend_markup = InlineKeyboardMarkup(trend_keyboard)
        
        trend_text = (
            "🏆 **قناة تـرنـد²⁰²٧ للمسابقات والجوائز**\n\n"
            f"تابع القناة الرسمية لتكون أول المشاركين والفائزين بالعروض الحصرية:\n👉 {TREND_CH}"
        )
        await query.message.reply_text(text=trend_text, reply_markup=trend_markup, parse_mode="Markdown")
        
    elif query.data == "dev_info":
        clean_dev = DEV_USER.replace("@", "").strip()
        dev_keyboard = [[InlineKeyboardButton("💬 مراسلة المطور الآن", url=f"tg://resolve?domain={clean_dev}")]]
        dev_markup = InlineKeyboardMarkup(dev_keyboard)
        
        dev_text = (
            "👨‍💻 **البطاقة التعريفية لمطور البوت**\n\n"
            f"للتواصل، الاستفسار، أو طلب تطوير بوتات خاصة، يمكنك مراسلة المطور عبر حسابه:\n👉 {DEV_USER}"
        )
        await query.message.reply_video(
            video=DEV_VIDEO,
            caption=dev_text,
            reply_markup=dev_markup,
            parse_mode="Markdown"
        )
        
    elif query.data == "support_info":
        clean_support = SUPPORT_CH.replace("@", "").strip()
        support_keyboard = [[InlineKeyboardButton("🛠️ دخول قسم الدعم", url=f"tg://resolve?domain={clean_support}")]]
        support_markup = InlineKeyboardMarkup(support_keyboard)
        
        support_text = (
            "🛠️ **مجموعة الدعم الفني والمساعدة**\n\n"
            f"إذا واجهتك أي مشكلة أو كان لديك اقتراح، تفضل بزيارة قناة الدعم:\n👉 {SUPPORT_CH}"
        )
        await query.message.reply_text(text=support_text, reply_markup=support_markup, parse_mode="Markdown")

    elif query.data == "back_to_main":
        # تنظيف وحذف رسالة القنوات الفرعية عند الضغط على زر العودة
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(f"Error deleting message: {e}")

# الدالة التشغيلية الرئيسية المحمية من التعليق السحابي
def main():
    if not TOKEN or "ضع_توكن_البوت" in TOKEN:
        print("❌ خطأ: يرجى وضع توكن البوت بشكل صحيح قبل التشغيل!")
        return

    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # [مهم جداً] تسجيل المعالجات لربط الأزرار والأوامر برمجياً بالسيرفر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("🚀 البوت ياسمين يعمل الآن بأعلى كفاءة واستجابة فورية...")
    
    # تشغيل مستقر ومتوافق تماماً مع خوادم Railway
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
    
