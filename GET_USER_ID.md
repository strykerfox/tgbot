# How to Get Your Telegram User ID

Your bot needs your User ID to send you notifications when users select products. Here's how to get it:

## Method 1: Using @userinfobot (Easiest)

1. Open Telegram
2. Search for **@userinfobot**
3. Click on it and send any message (like `/start`)
4. The bot will reply with your **User ID**
5. Copy the ID number

**Example output:**
```
Name: Sagar
User ID: 123456789
Username: @oceanallsea
```

Your **User ID** is the number in the `User ID:` line.

## Method 2: Using @getidsbot

1. Open Telegram
2. Search for **@getidsbot**
3. Send any message
4. It will show your User ID and other info

---

## Step-by-Step to Update Your Bot:

1. Get your User ID using one of the methods above
2. Open `.env` file in your Tgbot folder
3. Find this line: `OWNER_USER_ID=your_user_id_here`
4. Replace `your_user_id_here` with your actual User ID

**Example:**
```env
OWNER_USER_ID=123456789
```

5. Save the file
6. **RESTART THE BOT** - Stop the bot and run it again
7. Done! Now you'll receive messages when users select products

---

## Verification

After you update `.env` and restart the bot:

1. Send `/start` to your bot
2. Go to Premium → Click on any product
3. You should **immediately** receive a message with:
   - User details
   - Product selected
   - Link to message the user

If you don't receive it, check:
- ✅ User ID is correct (no spaces, just numbers)
- ✅ Bot is restarted after updating `.env`
- ✅ You haven't set a username for the bot (it should only have a token)

---

## Questions?

If notifications still aren't working:
1. Check the bot terminal for error messages
2. Make sure your User ID is just numbers (like: 123456789)
3. Restart the bot completely

Good luck! 🚀
