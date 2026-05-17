import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ضع توكن البوت الحقيقي هنا مباشرة بين علامات التنصيص لإنهاء مشاكل الـ InvalidToken
TOKEN = "ضع_توكن_بوتك_هنا"

WELCOME_VIDEO = os.getenv("WELCOME_VIDEO")
DEV_VIDEO = os.getenv("DEV_VIDEO")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "🌸 **مرحباً بك في بوت ياسمين الرسمي** 🌸\n\n"
        "يسعدنا انضمامك إلينا! يرجى استخدام الأزرار أدناه للتنقل "
        "بين خدماتنا، المسابقات، وقنوات الدعم المتاحة.\n\n"
        "✨ تصفح ممتع نتمناه لك!"
    )
    
    # روابط مباشرة وصريحة 100% تمنع ظهور الروابط الناقصة
    keyboard = [
        [
            InlineKeyboardButton("📜 Y.S", callback_data="ys_list"),
            InlineKeyboardButton("🏆 تـرنـد²⁰²٧", url="https://t.me")
        ],
        [
            InlineKeyboardButton("👨‍💻 المطور", callback_data="dev_info"),
            InlineKeyboardButton("🛠️ الدعم", url="https://t.me")
        ],
        [
            # ربط مباشر وصحيح لبوت ريتاج يفتحه داخل التطبيق فوراً
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

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "ys_list":
        # كتابة القنوات مباشرة داخل الكود لضمان عدم تعليق السيرفر في القراءة
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
        ys_markup = InlineKeyboardMarkup(ys_keyboard)
        
        await query.message.reply_text(
            text="📜 **قائمة القنوات التابعة لنا بالترتيب:**\nاضغط على أي قناة للانتقال إليها:",
            reply_markup=ys_markup,
            parse_mode="Markdown"
        )
        
    elif query.data == "dev_info":
        dev_text = (
            "👨‍💻 **البطاقة التعريفية لمطور البوت**\n\n"
            "للتواصل، الاستفسار، أو طلب تطوير بوتات خاصة، يمكنك مراسلة المطور عبر حسابه:\n👉 @shaheen_ys"
        )
        dev_keyboard = [[InlineKeyboardButton("💬 مراسلة المطور الآن", url="https://t.me")]]
        dev_markup = InlineKeyboardMarkup(dev_keyboard)
        
        await query.message.reply_video(
            video=DEV_VIDEO,
            caption=dev_text,
            reply_markup=dev_markup,
            parse_mode="Markdown"
        )

    elif query.data == "back_to_main":
        try:
            await query.message.delete()
        except:
            pass

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
    
