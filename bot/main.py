import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands.commands import start, exchangerate, history, help_command, unknown_command
from api.fixer_api import fetch_supported_currencies


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

fetch_supported_currencies()


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("exchangerate", exchangerate))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    application.run_polling()


if __name__ == '__main__':
    main()
