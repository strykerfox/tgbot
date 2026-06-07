"""
Telegram Bot — Welcome, language selection, and service navigation.
"""

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import (
    BOT_TOKEN,
    CHANNEL_LINK,
    DEFAULT_LANG,
    EXCHANGE_ADMIN_USERNAME,
    EXCHANGE_CHANNEL_LINK,
    LANGUAGES,
    OWNER_USER_ID,
    OWNER_USERNAME,
    PREMIUM_CHANNEL_LINK,
    t,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.user_data.get("lang", DEFAULT_LANG)


def language_keyboard(lang: str | None = None) -> InlineKeyboardMarkup:
    items = list(LANGUAGES.items())
    rows = [
        [
            InlineKeyboardButton(label, callback_data=f"lang_{code}")
            for code, label in items[i : i + 2]
        ]
        for i in range(0, len(items), 2)
    ]
    if lang:
        rows.append([InlineKeyboardButton(t(lang, "btn_back_menu"), callback_data="menu")])
    return InlineKeyboardMarkup(rows)


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t(lang, "btn_free"), callback_data="svc_free"),
            InlineKeyboardButton(t(lang, "btn_premium_bundles"), callback_data="svc_pb"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_exchange"), callback_data="svc_exchange"),
            InlineKeyboardButton(t(lang, "btn_image"), callback_data="svc_image"),
        ],
        [
            InlineKeyboardButton(t(lang, "btn_support"), url=f"https://t.me/{OWNER_USERNAME}"),
            InlineKeyboardButton(t(lang, "btn_change_lang"), callback_data="lang_pick"),
        ],
    ])


def premium_bundles_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t(lang, "btn_premium"), callback_data="svc_premium")],
        [InlineKeyboardButton(t(lang, "btn_bundles"), callback_data="svc_bundles")],
        [InlineKeyboardButton(t(lang, "btn_back_menu"), callback_data="menu")],
    ])


def back_to_menu_row(lang: str) -> list:
    return [InlineKeyboardButton(t(lang, "btn_back_menu"), callback_data="menu")]


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.effective_user.first_name
    text = t(DEFAULT_LANG, "welcome", name=name)
    markup = language_keyboard()

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")


async def show_language_picker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(context)
    text = t(lang, "language_pick")
    markup = language_keyboard(lang)

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(context)
    text = t(lang, "main_menu") + t(lang, "cta_footer")
    markup = main_menu_keyboard(lang)

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")
    elif update.message:
        await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_welcome(update, context)


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "lang" not in context.user_data:
        await send_welcome(update, context)
        return
    await show_main_menu(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_lang(context)
    await update.message.reply_text(
        t(lang, "help", owner=OWNER_USERNAME),
        parse_mode="Markdown",
    )


async def on_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = get_lang(context)

    # ── Language selection ────────────────────────────────────────────────
    if data == "lang_pick":
        await show_language_picker(update, context)
        return

    if data.startswith("lang_"):
        context.user_data["lang"] = data.removeprefix("lang_")
        await show_main_menu(update, context)
        return

    # ── Main menu ─────────────────────────────────────────────────────────
    if data == "menu":
        await show_main_menu(update, context)
        return

    # ── Premium & Bundles submenu (buttons only) ──────────────────────────
    if data == "svc_pb":
        await query.edit_message_text(
            t(lang, "pb_menu"),
            reply_markup=premium_bundles_keyboard(lang),
            parse_mode="Markdown",
        )
        return

    # ── Service detail views ──────────────────────────────────────────────
    if data == "svc_free":
        keyboard = [
            [InlineKeyboardButton(t(lang, "btn_join_channel"), url=CHANNEL_LINK)],
            back_to_menu_row(lang),
        ]
        await query.edit_message_text(
            f"{t(lang, 'free_title')}\n\n{t(lang, 'free_body')}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    if data == "svc_premium":
        keyboard = [
            [InlineKeyboardButton(t(lang, "btn_join_premium"), url=PREMIUM_CHANNEL_LINK)],
            [InlineKeyboardButton(t(lang, "btn_request_permission"), callback_data="req_premium")],
            [InlineKeyboardButton(t(lang, "btn_back_pb"), callback_data="svc_pb")],
        ]
        await query.edit_message_text(
            f"{t(lang, 'premium_title')}\n\n{t(lang, 'premium_body', owner=OWNER_USERNAME)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    if data == "svc_bundles":
        keyboard = [
            [InlineKeyboardButton(t(lang, "btn_contact_admin"), url=f"https://t.me/{OWNER_USERNAME}")],
            [InlineKeyboardButton(t(lang, "btn_back_pb"), callback_data="svc_pb")],
        ]
        await query.edit_message_text(
            f"{t(lang, 'bundles_title')}\n\n{t(lang, 'bundles_body')}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    if data == "svc_exchange":
        keyboard = [
            [InlineKeyboardButton(t(lang, "btn_request_join_exchange"), url=EXCHANGE_CHANNEL_LINK)],
            [InlineKeyboardButton(t(lang, "btn_verify_exchange_admin"), url=f"https://t.me/{EXCHANGE_ADMIN_USERNAME}")],
            back_to_menu_row(lang),
        ]
        await query.edit_message_text(
            f"{t(lang, 'exchange_title')}\n\n{t(lang, 'exchange_body', exchange_admin=EXCHANGE_ADMIN_USERNAME)}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    if data == "svc_image":
        keyboard = [
            [InlineKeyboardButton(t(lang, "btn_contact_admin"), url=f"https://t.me/{OWNER_USERNAME}")],
            back_to_menu_row(lang),
        ]
        await query.edit_message_text(
            f"{t(lang, 'image_title')}\n\n{t(lang, 'image_body')}",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )
        return

    # ── Request notifications to owner ──────────────────────────────────
    if data.startswith("req_"):
        service = data.removeprefix("req_")
        notify_keys = {
            "premium": "notify_premium",
            "bundles": "notify_bundles",
            "exchange": "notify_exchange",
            "image": "notify_image",
        }
        await notify_owner(update, context, t(lang, notify_keys[service]))
        await query.answer(t(lang, "notify_sent"), show_alert=True)
        return


async def notify_owner(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    service_label: str,
) -> None:
    owner_id = context.bot_data.get("owner_id")
    if not owner_id:
        return

    user = update.effective_user
    user_link = f"tg://user?id={user.id}"
    message = (
        f"{service_label}\n\n"
        f"👤 {user.first_name} {user.last_name or ''}\n"
        f"🆔 {user.id}\n"
        f"📱 @{user.username or 'no username'}\n\n"
        f"[Message user]({user_link})"
    )
    try:
        await context.bot.send_message(chat_id=owner_id, text=message, parse_mode="Markdown")
        logger.info("Notification sent to owner for %s (user %s)", service_label, user.id)
    except Exception as exc:
        logger.error("Failed to notify owner: %s", exc)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    if OWNER_USER_ID and OWNER_USER_ID != "your_user_id_here":
        application.bot_data["owner_id"] = int(OWNER_USER_ID)
    else:
        logger.warning("OWNER_USER_ID not set — owner notifications disabled")

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CallbackQueryHandler(on_callback))

    logger.info("Bot is starting...")
    logger.info("Menu text: %s", t(DEFAULT_LANG, "main_menu").split("\n")[0])
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
