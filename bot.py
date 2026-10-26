
import os
from urllib.parse import quote_plus
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎵 Welcome to Suno Song Bot!\n\n"
        "Send me a song name or artist to find it on YouTube."
    )


async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    song = update.message.text.strip()
    url = "https://www.youtube.com/results?search_query=" + quote_plus(song)

    keyboard = [
        [InlineKeyboardButton("▶️ Find Song", url=url)],
        [InlineKeyboardButton("📝 Do you want lyrics?", callback_data="lyrics")],
    ]

    await update.message.reply_text(
        f"🎧 Song: {song}\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "📝 Please send the song title and artist to find lyrics."
    )


def main():
    if not TOKEN:
        raise RuntimeError("Please configure TELEGRAM_BOT_TOKEN.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(lyrics, pattern="^lyrics$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_song))
    app.run_polling()


if __name__ == "__main__":
    main()
