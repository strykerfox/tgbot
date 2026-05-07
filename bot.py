"""
Main Telegram Bot Application
Handles user interactions and bot logic
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN, OWNER_USERNAME, OWNER_USER_ID, CHANNEL_LINK, FREE_ECOSYSTEM_DESCRIPTION, PREMIUM_DESCRIPTION, PREMIUM_PRODUCTS, DYNAMIC_DESCRIPTION

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start command - Shows welcome message with two main options
    """
    user_name = update.effective_user.first_name
    
    welcome_message = f"""
👋 *Welcome, {user_name}!*

I'm here to help you explore amazing content. Choose your path:

1️⃣ **Free Ecosystem** - Access quality content for free (with some security measures)
2️⃣ **Premium** - Get personalized support from our team

What would you like to do?
"""
    
    # Create inline keyboard with two options
    keyboard = [
        [InlineKeyboardButton("🎯 Explore Free Ecosystem", callback_data="free")],
        [InlineKeyboardButton("💎 Go Premium", callback_data="premium")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def free_ecosystem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle free ecosystem option
    """
    query = update.callback_query
    await query.answer()
    
    # Show free ecosystem description
    keyboard = [
        [InlineKeyboardButton("📺 Enter Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    channel_message = f"""
{FREE_ECOSYSTEM_DESCRIPTION}

━━━━━━━━━━━━━━━━━━━━

📺 **The One Streamer (General)**

Get to the One Streamer General channel - it has everything you need for free!
"""
    
    await query.edit_message_text(
        text=channel_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def premium_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle premium option - Show products list
    """
    query = update.callback_query
    await query.answer()
    
    # Create keyboard with product options
    keyboard = []
    for product_key, product_info in PREMIUM_PRODUCTS.items():
        button_text = f"{product_info['name']} - {product_info['price']}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"product_{product_key}")])
    
    # Add back button
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="start")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    premium_message = f"""
{PREMIUM_DESCRIPTION}

━━━━━━━━━━━━━━━━━━━━

📦 *Available Packages:*

Click on any package to get more details:
"""
    
    await query.edit_message_text(
        text=premium_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def product_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle product selection - Show product details and send notification to owner
    """
    query = update.callback_query
    await query.answer()
    
    # Extract product key from callback data
    product_key = query.data.split("_")[1] + "_" + query.data.split("_")[2]
    
    product_info = PREMIUM_PRODUCTS.get(product_key)
    
    if not product_info:
        await query.edit_message_text(text="❌ Product not found!")
        return
    
    # Get user information
    user = update.effective_user
    user_link = f"tg://user?id={user.id}"
    
    # Store selected product for note capture
    context.user_data['selected_product'] = product_key
    
    # Prepare product-specific message
    product_description = product_info['description']
    
    # Add dynamic description only for products 1-4 (content packages)
    if product_info['category'] == 'content':
        full_description = f"{product_description}\n\n{DYNAMIC_DESCRIPTION}"
    else:
        full_description = product_description
    
    # Message to show user
    user_message = f"""
✅ *You Selected: {product_info['name']}*

💰 Price: {product_info['price']}

📝 Description:
{full_description}

━━━━━━━━━━━━━━━━━━━━

💬 *Want to add any notes or requests?*

Reply below with any special requests, questions, or details. Then click "Contact Attendant" below.

Or directly click the button to contact our team!
"""
    
    keyboard = [
        [InlineKeyboardButton("👤 Contact Personal Attendant", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("⬅️ Back to Products", callback_data="premium")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=user_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # IMMEDIATELY SEND NOTIFICATION TO OWNER
    try:
        # Get your Telegram user ID (you need to set this in config)
        owner_id = context.bot_data.get('owner_id')
        
        if owner_id:
            # Create notification message
            owner_notification = f"""
🔔 *New Premium Inquiry*

👤 User: {user.first_name} {user.last_name or ''}
🆔 User ID: {user.id}
📱 Username: @{user.username or 'No username'}

━━━━━━━━━━━━━━━━━━━━

📦 *Product Selected:*
{product_info['name']}
💰 Price: {product_info['price']}

📝 *Description:*
{full_description}

━━━━━━━━━━━━━━━━━━━━

[👤 Message this user]({user_link})
"""
            
            # Send to owner
            await context.bot.send_message(
                chat_id=owner_id,
                text=owner_notification,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Sent product inquiry notification to owner. Product: {product_info['name']}")
    except Exception as e:
        logger.error(f"⚠️ Could not send notification to owner: {e}")


async def handle_user_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Capture user's custom notes/requests and send to owner
    """
    if update.message and update.message.text:
        # Store the user's notes
        context.user_data['user_notes'] = update.message.text
        
        # Get stored product info
        product_key = context.user_data.get('selected_product')
        product_info = PREMIUM_PRODUCTS.get(product_key)
        
        if product_info:
            user = update.effective_user
            user_link = f"tg://user?id={user.id}"
            
            # Get full description based on product category
            product_description = product_info['description']
            if product_info['category'] == 'content':
                full_description = f"{product_description}\n\n{DYNAMIC_DESCRIPTION}"
            else:
                full_description = product_description
            
            # Updated message with user notes
            owner_notification = f"""
🔔 *New Premium Inquiry - With User Notes*

👤 User: {user.first_name} {user.last_name or ''}
🆔 User ID: {user.id}
📱 Username: @{user.username or 'No username'}

━━━━━━━━━━━━━━━━━━━━

📦 *Product Selected:*
{product_info['name']}
💰 Price: {product_info['price']}

📝 *Description:*
{full_description}

━━━━━━━━━━━━━━━━━━━━

💬 *User's Notes/Requests:*
{context.user_data['user_notes']}

━━━━━━━━━━━━━━━━━━━━

[👤 Message this user]({user_link})
"""
            
            response = f"""
✅ *Your Request Received!*

📦 Product: {product_info['name']}
📝 Your Notes: {context.user_data['user_notes']}

Your inquiry with all details has been recorded. A personal attendant will reach out to you shortly!

Thank you! 🎉
"""
            
            # Send response to user
            await update.message.reply_text(response, parse_mode="Markdown")
            
            # SEND UPDATED NOTIFICATION TO OWNER
            try:
                owner_id = context.bot_data.get('owner_id')
                if owner_id:
                    await context.bot.send_message(
                        chat_id=owner_id,
                        text=owner_notification,
                        parse_mode="Markdown"
                    )
                    logger.info(f"✅ Sent product inquiry with notes to owner. Product: {product_info['name']}")
            except Exception as e:
                logger.error(f"⚠️ Could not send notification to owner: {e}")
        else:
            await update.message.reply_text("❌ Error: Please first select a product. Reply after clicking on a premium product.")


async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Go back to start menu
    """
    query = update.callback_query
    await query.answer()
    
    user_name = query.from_user.first_name
    
    welcome_message = f"""
👋 *Welcome, {user_name}!*

I'm here to help you explore amazing content. Choose your path:

1️⃣ **Free Ecosystem** - Access quality content for free (with some security measures)
2️⃣ **Premium** - Get personalized support from our team

What would you like to do?
"""
    
    keyboard = [
        [InlineKeyboardButton("🎯 Explore Free Ecosystem", callback_data="free")],
        [InlineKeyboardButton("💎 Go Premium", callback_data="premium")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help command - Show help information
    """
    help_text = """
📖 *How to use this bot:*

/start - Start the bot and see options
/help - Show this help message

🎯 *Free Path:*
- Explore our free ecosystem
- Get access to our general channel
- All free, no cost!

💎 *Premium Path:*
- Browse premium packages
- Contact our personal attendant
- Personalized experience

Any questions? Contact: @{owner_username}
""".format(owner_username=OWNER_USERNAME)
    
    await update.message.reply_text(help_text, parse_mode="Markdown")


def main() -> None:
    """
    Start the bot
    """
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Store owner_id in bot_data for use in handlers
    if OWNER_USER_ID and OWNER_USER_ID != 'your_user_id_here':
        application.bot_data['owner_id'] = int(OWNER_USER_ID)
    else:
        logger.warning("⚠️ OWNER_USER_ID not set in .env - notifications will not be sent to owner")
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handlers for buttons
    application.add_handler(CallbackQueryHandler(free_ecosystem, pattern="^free$"))
    application.add_handler(CallbackQueryHandler(premium_products, pattern="^premium$"))
    application.add_handler(CallbackQueryHandler(product_details, pattern="^product_"))
    application.add_handler(CallbackQueryHandler(back_to_start, pattern="^start$"))
    
    # Add message handler for user notes (must be after callback handlers)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_notes))
    
    # Start the Bot
    logger.info("🤖 Bot is starting...")
    application.run_polling()


if __name__ == '__main__':
    main()
