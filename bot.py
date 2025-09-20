import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"🤖 Hello {user.first_name}!\n\n"
        "I am your File Rename Bot. I can help you:\n\n"
        "• Remove specific words from file names\n"
        "• Add prefix/suffix to file names\n"
        "• Replace words in file names\n"
        "• Work with both public and private channels\n\n"
        "Use /help for instructions or /rename to start!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when command /help is issued."""
    help_text = """
📋 **Available Commands:**
/start - Start the bot
/help - Show this help message  
/rename - Start file renaming process

🚀 **How to Use:**
1. Add me to your channel as admin with edit permissions
2. Use /rename and follow the prompts
3. I'll guide you through the process

🔒 **For Private Channels:**
• Get channel ID by forwarding any message to @userinfobot
• Use format: -1001234567890 (starts with -100)

🔢 **Message IDs:**
• Forward messages to @userinfobot to get IDs
• Use format: 123 to 145 for ranges

⚠️ **Requirements:**
• Bot must be admin in your channel
• Bot needs 'Edit messages' permission
"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def rename_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the rename process."""
    await update.message.reply_text(
        "🔄 **File Rename Process Started**\n\n"
        "Please send me the word you want to find in file names.\n\n"
        "Examples:\n"
        "• 'sample' - to find this word\n"
        "• 'remove_this' - to remove this text\n"
        "• 'old_text' - to replace with new text\n\n"
        "I'll ask you what to do with it next.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages."""
    user_text = update.message.text
    
    # Ignore commands
    if user_text.startswith('/'):
        return
    
    # Simulate processing
    await update.message.reply_text(
        f"✅ Got it! You sent: '{user_text}'\n\n"
        "In the full version, I would:\n"
        "1. Ask for your channel username/ID\n"
        "2. Ask what action to perform (remove/add/replace)\n"
        "3. Ask for message range to process\n"
        "4. Execute the changes in your channel\n\n"
        "This basic version confirms I'm working!",
        parse_mode="Markdown"
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error("Error occurred:", exc_info=context.error)
    try:
        await update.message.reply_text("❌ Sorry, something went wrong. Please try /start again.")
    except:
        pass

def main():
    """Start the bot."""
    # Get bot token from environment variable
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN environment variable is missing!")
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not found!")
        return
    
    print(f"✅ Starting bot with token: {token[:10]}...{token[-5:]}")
    
    try:
        # Create application
        application = Application.builder().token(token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("rename", rename_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        # Start the bot
        print("✅ Bot is starting in polling mode...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        print(f"❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
