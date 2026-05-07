# 🔧 EXACT COMMANDS TO DEPLOY

Copy-paste these commands exactly to deploy your bot to Railway!

---

## Step 1: Configure Git (First Time Only)

```bash
cd /Users/sagar/Tgbot

git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"
```

**Replace:**
- `Your Name` = Your actual name
- `your.email@gmail.com` = Your email

---

## Step 2: Add GitHub Remote

```bash
git remote add origin https://github.com/YOUR_USERNAME/Tgbot.git
git branch -M main
git push -u origin main
```

**Replace:**
- `YOUR_USERNAME` = Your GitHub username

**What to do:**
1. Create account at https://github.com
2. Create new repo named "Tgbot"
3. Replace YOUR_USERNAME above
4. Run the commands

---

## Step 3: Deploy on Railway

1. Go to https://railway.app
2. Click "Login" → Select "GitHub"
3. Authorize GitHub
4. Click "New Project" → "Deploy from GitHub"
5. Select "Tgbot" repository
6. Click "Deploy"

---

## Step 4: Add Environment Variables in Railway

In Railway dashboard → Your project → Settings/Variables

Add these 5 variables exactly:

```
TELEGRAM_BOT_TOKEN=8600220216:AAEW0yTlJPO27rru9-u-8-ub2GCCcKDxZmo
OWNER_USERNAME=oceanallsea
OWNER_USER_ID=7872021644
CHANNEL_USERNAME=your_channel_username
CHANNEL_LINK=https://t.me/+laTZFTDKCLhjZjk9
```

Then click "Deploy"

---

## Step 5: Verify Deployment

Send `/start` to your bot in Telegram
Should respond immediately! ✓

---

## Future Updates (After First Deployment)

Anytime you want to update your bot:

```bash
cd /Users/sagar/Tgbot

git add .
git commit -m "Your update description"
git push
```

Railway automatically redeploys! ⚡

---

## Check Your Bot Status

```bash
git status          # See current changes
git log             # See commit history
git remote -v       # See GitHub connection
```

---

## That's It!

Follow these steps and your bot will be live! 🚀
