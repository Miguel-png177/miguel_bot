import logging
import random
import os
from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = ''

WALKS = [
    "https://youtu.be/nd7YW_D76wc",
    "https://youtu.be/9Yv4WGMV5RC",
    "https://youtu.be/cUcTNtNWq58"
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    chat_id = update.effective_chat.id
    keyboard = ReplyKeyboardMarkup([
        ["📹 YouTube", "ℹ️ О канале"],
        ["🎥 Прогулка", "🎞 Плейлисты"],
        ["📬 Контакты"]
    ], resize_keyboard=True)

    if os.path.exists("logo.png"):
        try:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=InputFile("logo.png"),
                caption="👋 Добро пожаловать в бот канала \"Прогулки с Мигелем\"!\n\nНажмите кнопку ниже, чтобы узнать больше или посмотреть прогулку.",
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка при отправке фото: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text="👋 Добро пожаловать в бот канала \"Прогулки с Мигелем\"!\n\nНажмите кнопку ниже, чтобы узнать больше или посмотреть прогулку.",
                reply_markup=keyboard
            )
    else:
        logger.warning("Файл logo.png не найден")
        await context.bot.send_message(
            chat_id=chat_id,
            text="👋 Добро пожаловать в бот канала \"Прогулки с Мигелем\"!\n\n(Логотип не найден)\n\nНажмите кнопку ниже, чтобы узнать больше или посмотреть прогулку.",
            reply_markup=keyboard
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id

    if text == "📹 YouTube":
        await update.message.reply_text("Мой канал на YouTube: https://www.youtube.com/@WalkingwithMiguel")

    elif text == "ℹ️ О канале":
        about = (
            "Гуляем вместе. Пройдем по разным районам с оживленными улицами и окунемся вместе в течение жизни современного города.\n\n"
            "Это не исторический канал. Этот канал о сегодняшней жизни города в его настоящем.\n\n"
            "И слов не надо, всё за нас скажут сегодняшние герои города: его люди, дома и бульвары.\n\n"
            "Если вам нравится видео, подписывайтесь и ставьте лайки."
        )
        await update.message.reply_text(about)

    elif text == "🎥 Прогулка":
        walk = random.choice(WALKS)
        await update.message.reply_text(f"🎬 Сегодняшняя прогулка: {walk}")

    elif text == "🎞 Плейлисты":
        playlists = (
            "🎒 <b>Прогулки по улицам Москвы</b>\nhttps://www.youtube.com/playlist?list=PLTs0TNel9HD0feW55a6WGqgLCJIn98wyz\n\n"
            "🌆 <b>Города России</b>\nhttps://www.youtube.com/playlist?list=PLTs0TNel9HD2AcLmQnm6LW59iEM37iogt\n\n"
            "🚗 <b>In Drive / на автомобиле</b>\nhttps://www.youtube.com/playlist?list=PLTs0TNel9HD3csK5oHx5bmYIZ3KsqQHOj"
        )
        await update.message.reply_text(playlists, parse_mode="HTML")

    elif text == "📬 Контакты":
        await update.message.reply_text("📩 Написать мне: https://t.me/Migel177")

    else:
        await update.message.reply_text("Выберите команду с клавиатуры ⬇️")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()
