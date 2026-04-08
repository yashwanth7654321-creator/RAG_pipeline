import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from source_code.pipeline import ask

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Commands
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I am your RAG bot.\n\n"
        "Use /ask <your question>"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n"
        "/ask <question> - Ask something\n"
        "/help - Show help"
    )


# -----------------------------
# Main RAG handler
# -----------------------------
async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conn = context.application.bot_data["conn"]
    cursor = context.application.bot_data["cursor"]
    collection = context.application.bot_data["collection"]

    if not context.args:
        await update.message.reply_text("❗ Please provide a question.\nExample: /ask What is leave policy?")
        return
    
    query = " ".join(context.args)
    
    await update.message.reply_text("⏳ Thinking...")
    
    try:
        answer = ask(query, conn, cursor, user_id, collection)
        await update.message.reply_text(answer)
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


# -----------------------------
# Handle normal messages
# -----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    query = update.message.text
    conn = context.application.bot_data["conn"]
    cursor = context.application.bot_data["cursor"]
    collection = context.application.bot_data["collection"]
    
    await update.message.reply_text("⏳ Thinking...")
    
    try:
        answer = ask(query, conn, cursor, user_id, collection)
        await update.message.reply_text(answer)
        print(user_id)
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def stop(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Conversation ended")
# -----------------------------
# Run bot
# -----------------------------
def run_bot(token, conn, cursor, collection):
    app = ApplicationBuilder().token(token).build()
    app.bot_data["conn"] = conn
    app.bot_data["cursor"] = cursor
    app.bot_data["collection"] = collection
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("stop", stop))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Bot is running...")
    app.run_polling()