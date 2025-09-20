import os
import logging
import telebot
from telebot import types

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN environment variable is missing!")
    print("❌ ERROR: TELEGRAM_BOT_TOKEN not found!")
    exit(1)

# Create bot instance
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Send welcome message when command /start is issued."""
    user = message.from_user
    bot.reply_to(message, 
        f"🤖 Hello {user.first_name}!\n\n"
        "I am your File Rename Bot. I can help you:\n\n"
        "• Remove specific words from file names\n"
        "• Add prefix/suffix to file names\n"
        "• Replace words in file names\n"
        "• Work with both public and private channels\n\n"
        "Use /help for instructions or /rename to start!"
    )

@bot.message_handler(commands=['help'])
def send_help(message):
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
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['rename'])
def start_rename(message):
    """Start the rename process."""
    bot.reply_to(message,
        "🔄 **File Rename Process Started**\n\n"
        "Please send me the word you want to find in file names.\n\n"
        "Examples:\n"
        "• 'sample' - to find this word\n"
        "• 'remove_this' - to remove this text\n"
        "• 'old_text' - to replace with new text\n\n"
        "I'll ask you what to do with it next.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Handle all text messages."""
    user_text = message.text
    
    # Ignore commands
    if user_text.startswith('/'):
        return
    
    # Simulate processing
    bot.reply_to(message,
        f"✅ Got it! You sent: '{user_text}'\n\n"
        "In the full version, I would:\n"
        "1. Ask for your channel username/ID\n"
        "2. Ask what action to perform (remove/add/replace)\n"
        "3. Ask for message range to process\n"
        "4. Execute the changes in your channel\n\n"
        "This basic version confirms I'm working! 🎉",
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print(f"✅ Starting bot with token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")
    print("✅ Bot is starting in polling mode...")
    bot.infinity_polling()
