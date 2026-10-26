import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- تنظیمات ---
BOT_TOKEN = "8644615067:AAEfRUsRGX1857nwHX_JZV-YqVFu-tL4Arg"
ADMIN_GROUP_ID = -1004395843163

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

message_map = {}

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    header = f"📩 پیام از: {user.full_name}\n🆔 آیدی: {user.id}\n\n"
    try:
        sent_msg = await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=header + (message.text or "پیام غیرمتنی")
        )
        message_map[sent_msg.message_id] = user.id
        await message.reply_text("✅ پیام شما دریافت شد. به زودی پاسخ می‌دهیم.")
    except Exception as e:
        logging.error(f"Error forwarding message: {e}")
        await message.reply_text("❌ متأسفانه در ارسال پیام خطایی رخ داد.")

async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.reply_to_message:
        replied_msg_id = message.reply_to_message.message_id
        user_id = message_map.get(replied_msg_id)
        if user_id:
            try:
                await context.bot.send_message(chat_id=user_id, text=message.text)
                await message.reply_text("✅ پاسخ شما برای کاربر ارسال شد.")
            except Exception as e:
                logging.error(f"Error sending reply: {e}")
                await message.reply_text("❌ خطا در ارسال پاسخ.")
        else:
            await message.reply_text("⚠️ این پیام به هیچ کاربری متصل نیست.")
    else:
        await message.reply_text("ℹ️ برای پاسخ به کاربر، روی پیام او ریپلای کنید.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, handle_user_message))
    app.add_handler(MessageHandler(filters.Chat(ADMIN_GROUP_ID) & filters.REPLY, handle_admin_reply))
    print("Support Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
