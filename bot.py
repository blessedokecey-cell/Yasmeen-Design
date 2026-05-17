import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تفعيل تسجيل الأخطاء البرمجية
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# قراءة التوكن من متغيرات البيئة في Railway
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")

# جلب روابط الفيديوهات من المتغيرات
WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")
DEV_VIDEO = os.getenv("DEV_VIDEO")

# دالة الترحيب الأساسية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
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

# الدالة المعدلة والمضمونة لمعالجة ضغطات الأزرار داخلياً بالكامل
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    # [مهم جداً] تأكيد فوري ومضمون لاستقبال الضغطة لحل مشكلة التجمد والتعليق
    await query.answer()

    # 1. زر قائمة قنوات Y.S
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
            text="📜 **قائمة القنوات التابعة لنا بالترتيب:**\nاضغط على أي قناة للانتقال إليها:",
            reply_markup=InlineKeyboardMarkup(ys_keyboard),
            parse_mode="Markdown"
        )
        
    # 2. زر ترند
    elif query.data == "trend_info":
        trend_text = (
            "🏆 **قناة تـرنـد²⁰²٧ للمسابقات والجوائز**\n\n"
            "تابع القناة الرسمية لتكون أول المشاركين والفائزين بالعروض الحصرية:\n👉 @fi1_oo"
        )
        trend_keyboard = [[InlineKeyboardButton("🚀 دخول قناة التريند", url="https://t.mefi1_oo")]]
        await query.message.reply_text(text=trend_text, reply_markup=InlineKeyboardMarkup(trend_keyboard), parse_mode="Markdown")
        
    # 3. زر المطور
    elif query.data == "dev_info":
        dev_text = (
            "👨‍💻 **البطاقة التعريفية لمطور البوت**\n\n"
            "للتواصل، الاستفسار، أو طلب تطوير بوتات خاصة، يمكنك مراسلة المطور عبر حسابه:\n👉 @shaheen_ys"
        )
        dev_keyboard = [[InlineKeyboardButton("💬 مراسلة المطور الآن", url="https://t.meshaheen_ys")]]
        await query.message.reply_video(
            video=DEV_VIDEO,
            caption=dev_text,
            reply_markup=InlineKeyboardMarkup(dev_keyboard),
            parse_mode="Markdown"
        )
        
    # 4. زر الدعم
    elif query.data == "support_info":
        support_text = (
            "🛠️ **قسم الدعم الفني والمساعدة**\n\n"
            "إذا واجهتك أي مشكلة أو كان لديك اقتراح، تفضل بزيارة قناة الدعم:\n👉 @shaheen_ys"
        )
        support_keyboard = [[InlineKeyboardButton("🛠️ دخول قسم الدعم", url="https://t.meshaheen_ys")]]
        await query.message.reply_text(text=support_text, reply_markup=InlineKeyboardMarkup(support_keyboard), parse_mode="Markdown")

    # 5. زر ريتاج
    elif query.data == "retaj_info":
        retaj_text = (
            "👑 **الملكة ريتاج (Ret_QueenBot)**\n\n"
            "يمكنك الآن الانتقال وتصفح خدمات بوت ريتاج المميزة مباشرة عبر الزر أدناه:"
        )
        retaj_keyboard = [[InlineKeyboardButton("🤖 الدخول إلى بوت ريتاج", url="https://t.meRet_QueenBot")]]
        await query.message.reply_text(text=retaj_text, reply_markup=InlineKeyboardMarkup(retaj_keyboard), parse_mode="Markdown")

    # زر العودة لحذف القائمة
    elif query.data == "back_to_main":
        try:
            await query.message.delete()
        except:
            pass

def main():
    if not TOKEN:
        print("❌ خطأ: التوكن غير موجود في متغيرات البيئة!")
        return

    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("🚀 البوت ياسمين يعمل بكفاءة قصوى واستقرار كامل...")
    # [تحديث الإغلاق] تم تعديل هذه الدالة لتعمل بشكل متزامن دائم على خوادم ريلواي لمنع تعليق الضغطات
    application.run_polling()

if __name__ == "__main__":
    main()
    
