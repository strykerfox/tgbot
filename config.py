"""
Configuration file for the Telegram Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OWNER_USERNAME = os.getenv("OWNER_USERNAME")
OWNER_USER_ID = os.getenv("OWNER_USER_ID")  # Your Telegram User ID for receiving messages
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")

# Premium Products with pricing
PREMIUM_PRODUCTS = {
    "product_1": {
        "name": "🌟 Starter",
        "price": "$5",
        "description": "Entry-level package with essential content access.",
        "category": "content"
    },
    "product_2": {
        "name": "📚 Beginner",
        "price": "$8",
        "description": "Growing package with expanded content library.",
        "category": "content"
    },
    "product_3": {
        "name": "🚀 Pro",
        "price": "$12",
        "description": "Professional tier with premium content collections.",
        "category": "content"
    },
    "product_4": {
        "name": "👑 Pro Max",
        "price": "$15",
        "description": "Ultimate content access with priority support.",
        "category": "content"
    },
    "product_5": {
        "name": "🤖 Content Bot",
        "price": "$50 (Monthly - $30)",
        "description": "This bot has all the links and videos at one place, just like a website. The subscription monthly fee is used to refill the contents, we keep very low margins :)",
        "category": "bot"
    }
}

# Dynamic description for options 1-4
DYNAMIC_DESCRIPTION = """
These options up to 4th will get you a set of contents which you can receive as you like - a cloud link or directly in DM. 

Attendant will guide you through the process.
"""

# Free Ecosystem Info
FREE_ECOSYSTEM_DESCRIPTION = """
🎯 *Explore the Free Ecosystem*

We offer a friendly environment with some security routings to keep your experience safe and secure. Access all the essential content without any cost!

✅ Community Support
✅ Regular Updates
✅ Security Assured
"""

# Premium Info
PREMIUM_DESCRIPTION = """
💎 *Go Premium*

You are not purchasing from this bot directly. First, you'll have a **personal human attendant** who will:

👤 Answer all your questions
🎯 Provide personalized recommendations
💬 Ensure a great experience
🚀 Guide you through the process

Let's connect and discuss your needs!
"""
