import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# تفعيل تسجيل الأخطاء البرمجية
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# جلب البيانات والمتغيرات من لوحة تحكم Railway
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")
DEV_VIDEO = os.getenv("DEV_VIDEO")

# دالة الترحيب الأساسية عند إرسال /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
    # توزيع هندسي متناسق وأنيق للأزرار التفاعلية الداخلية بالكامل
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
            InlineKeyboardButton("👑 ريتاج", callback_data="retaj_info")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_video(
        video=WELCOME_VIDEO,
        caption=welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# الدالة البرمجية المستقرة لمعالجة ضغطات الأزرار داخلياً بلمح البصر
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    # إنهاء حالة الانتظار والتحميل في الزر فوراً لمنع التجمد
    await query.answer()

    # 1. عند الضغط على زر Y.S (قائمة القنوات التابعة لكم)
    if query.data == "ys_list":
        channels = [
            "@EmpireBoosts", "@ShadowNums", "@iconvx_pro", "@wrdxix", "@cvipx", 
            "@DesignArsenalAssets", "@shaheen_fot", "@DesignArsenalApps", "@DesignArsenalPacks", 
            "@DesignArsenalSupport", "@nikvxix", "@DesignArsenalNew", "@vixhdix", "@knozxix", "@krxvix"
        ]
        
        ys_buttons = []
        for ch in channels:
            clean_ch = ch.replace("@", "").strip()
            ys_buttons.append(InlineKeyboardButton(text=f"📢 {ch}", url=f"https://t.me{clean_ch}"))
        
        ys_keyboard = [ys_buttons[i:i + 2] for i in range(0, len(ys_buttons), 2)]
        ys_keyboard.append([InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main")])
        
        await query.message.reply_text(
            text="📜 **قائمة القنوات التابعة لنا بالترتيب:**\nاضغط على أي قناة للانتقال إليها فوراً:",
            reply_markup=InlineKeyboardMarkup(ys_keyboard),
            parse_mode="Markdown"
        )
        
    # 2. عند الضغط على زر ترند2027 (تم دمج يوزر @f1_oo المحدث)
    elif query.data == "trend_info":
        trend_text = (
            "🏆 **قناة تـرنـد²⁰²٧ للمسابقات والجوائز**\n\n"
            "تابع القناة الرسمية لتكون أول المشاركين والفائزين بالعروض الحصرية:\n👉 @f1_oo"
        )
        trend_keyboard = [[InlineKeyboardButton("🚀 دخول قناة التريند", url="https://t.mef1_oo")]]
        await query.message.reply_text(text=trend_text, reply_markup=InlineKeyboardMarkup(trend_keyboard), parse_mode="Markdown")
        
    # 3. عند الضغط على زر المطور (تم دمج يوزر @Y9_S4 المحدث)
    elif query.data == "dev_info":
        dev_text = (
            "👨‍💻 **البطاقة التعريفية لمطور البوت**\n\n"
            "للتواصل، الاستفسار، أو طلب تطوير بوتات خاصة، يمكنك مراسلة المطور عبر حسابه المباشر:\n👉 @Y9_S4"
        )
        dev_keyboard = [[InlineKeyboardButton("💬 مراسلة المطور الآن", url="https://t.meY9_S4")]]
        await query.message.reply_video(
            video=DEV_VIDEO,
            caption=dev_text,
            reply_markup=InlineKeyboardMarkup(dev_keyboard),
            parse_mode="Markdown"
        )
        
    # 4. عند الضغط على زر الدعم (تم دمج يوزر @shaheen_ys المحدث)
    elif query.data == "support_info":
        support_text = (
            "🛠️ **قسم الدعم الفني والمساعدة**\n\n"
            "إذا واجهتك أي مشكلة أو كان لديك اقتراح، تفضل بزيارة قناة الدعم المباشرة:\n👉 @shaheen_ys"
        )
        support_keyboard = [[InlineKeyboardButton("🛠️ دخول قسم الدعم", url="https://t.meshaheen_ys")]]
        await query.message.reply_text(text=support_text, reply_markup=InlineKeyboardMarkup(support_keyboard), parse_mode="Markdown")

    # 5. عند الضغط على زر ريتاج
    elif query.data == "retaj_info":
        retaj_text = (
            "👑 **الملكة ريتاج (Ret_QueenBot)**\n\n"
            "يمكنك الآن الانتقال وتصفح خدمات بوت ريتاج المميزة مباشرة عبر الزر أدناه:"
        )
        retaj_keyboard = [[InlineKeyboardButton("🤖 الدخول إلى بوت ريتاج", url="https://t.meRet_QueenBot")]]
        await query.message.reply_text(text=retaj_text, reply_markup=InlineKeyboardMarkup(retaj_keyboard), parse_mode="Markdown")

    # زر العودة الفرعي لحذف الرسالة وتنظيف الشاشة
    elif query.data == "back_to_main":
        try:
            await query.message.delete()
        except Exception as e:
            logger.error(f"Error deleting message: {e}")

# التهيئة المعمارية المستقرة والمحمية للتشغيل على Railway
def main():
    if not TOKEN:
        print("❌ خطأ: التوكن مفقود في لوحة تحكم المتغيرات بـ Railway!")
        return

    # استخدام البناء القياسي المباشر لضمان تماسك الجلسة السحابية
    application = ApplicationBuilder().token(TOKEN).build()
    
    # ربط وتثبيت معالجات الأوامر والضغطات بشكل إلزامي ومحمي
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("🚀 البوت ياسمين نشط ومستقر الآن بأعلى دقة برمجية...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
    
