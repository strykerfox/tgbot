# 🤖 Telegram Bot - Free Ecosystem & Premium

A fully functional Telegram bot that manages a free ecosystem channel and premium product inquiries with personalized human attendant support.

## ✨ Features

- 🎯 Welcome screen with two main options
- 🆓 Free ecosystem pathway with channel access
- 💎 Premium products with pricing and descriptions
- 👤 Personal attendant connection for premium inquiries
- 📱 Beautiful inline buttons and organized UI
- 🔐 Environment-based configuration (no hardcoding sensitive data)

## 📋 Prerequisites

- Python 3.8+
- Telegram account
- A Telegram Bot Token (from BotFather)

## 🚀 Quick Start

### 1. Get Your Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` command
3. Follow the steps and get your **Bot Token**
4. Save the token for later

### 2. Setup Your Environment

```bash
# Clone/Setup the project
cd /Users/sagar/Tgbot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure the Bot

Edit `.env` file and add:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
OWNER_USERNAME=your_telegram_username
CHANNEL_USERNAME=your_channel_name
CHANNEL_LINK=https://t.me/your_channel_link
```

**Example:**
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ1234567890
OWNER_USERNAME=yourname
CHANNEL_USERNAME=your_channel
CHANNEL_LINK=https://t.me/your_channel
```

### 4. Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 Bot is starting...
```

### 5. Test in Telegram

- Open Telegram
- Search for your bot (the name you gave BotFather)
- Send `/start`
- You should see the welcome menu with two buttons!

## 📁 Project Structure

```
Tgbot/
├── bot.py              # Main bot application
├── config.py           # Configuration & constants
├── requirements.txt    # Python dependencies
├── .env               # Your sensitive configuration (don't share!)
├── .env.example       # Example configuration
└── README.md          # This file
```

## 🎮 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot, see welcome menu |
| `/help` | Show help information |

## 🔘 Button Flows

### Free Ecosystem Path:
1. Click "🎯 Explore Free Ecosystem"
2. See description about free ecosystem
3. Click "📺 Enter Channel" → Goes to your channel
4. Click "⬅️ Back" → Return to main menu

### Premium Path:
1. Click "💎 Go Premium"
2. See premium description
3. View available products with prices
4. Click on a product
5. See product details
6. Click "👤 Contact Personal Attendant" → Opens DM with you
7. Can click "⬅️ Back" to see more products

## 🛠️ Customization

### Add More Premium Products

Edit `config.py` and add to `PREMIUM_PRODUCTS`:

```python
PREMIUM_PRODUCTS = {
    "product_1": {
        "name": "🌟 Your Product Name",
        "price": "$XX.XX",
        "description": "Your product description here"
    },
    # Add more products...
}
```

### Customize Messages

Edit the messages in `bot.py`:
- `FREE_ECOSYSTEM_DESCRIPTION` - Free ecosystem info
- `PREMIUM_DESCRIPTION` - Premium info
- Welcome message in `start()` function

### Change Channel Link

Update in `.env`:
```env
CHANNEL_LINK=https://t.me/your_new_channel
```

## 🌐 Deployment (Optional - For 24/7 Running)

If you want the bot to run 24/7, deploy to:

### Free Options:
1. **Railway.app** - Free tier available
2. **Render** - Free tier with limitations
3. **PythonAnywhere** - Free tier
4. **Heroku** - No longer free, but previously popular

### Easy Deployment to Railway:

1. Push your code to GitHub
2. Go to railway.app
3. Connect your GitHub repo
4. Add environment variables
5. Deploy!

(We can set this up later if needed)

## 🐛 Troubleshooting

### Bot not responding?

1. Check if `.env` file has correct token
2. Verify token is valid from BotFather
3. Check internet connection
4. Look for error messages in terminal

### Button links not working?

1. Verify channel username in `.env`
2. Make sure channel exists and is public/accessible
3. Check username format (should be without @)

## 📞 Support

For issues, check:
- `.env` configuration
- Bot token validity
- Internet connection
- Python version (3.8+)

## 📝 License

This project is open for personal use. Modify and customize as needed!

---

**Happy botting! 🚀**
