from telegram import Update
from telegram.ext import ContextTypes
from api.fixer_api import get_exchange_rate, get_supported_currencies
from db.db_control import save_exchange_rate_history, get_exchange_rate_history


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I am currency monitoring bot. I can check exchange rates and show your requests history. Check /help for more info')


async def exchangerate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text('Usage: /exchangerate base_currency target_currency')
        return

    base_currency, target_currency = context.args
    supported_currencies = get_supported_currencies()

    if base_currency not in supported_currencies or target_currency not in supported_currencies:
        await update.message.reply_text('One or both of the currencies are not supported.')
        return

    rate = get_exchange_rate(base_currency, target_currency)

    if rate is not None:
        save_exchange_rate_history(update.message.from_user.id, base_currency, target_currency, rate)
        await update.message.reply_text(f'Exchange rate from {base_currency} to {target_currency} is {rate}')
    else:
        await update.message.reply_text('Failed to fetch exchange rate.')


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    history = get_exchange_rate_history(user_id)

    if not history:
        await update.message.reply_text('You have no exchange rate history.')
        return

    history_text = "Your exchange rate history:\n"
    for entry in history:
        history_text += f"{entry.timestamp}: {entry.base_currency} -> {entry.target_currency} = {entry.exchange_rate}\n"

    await update.message.reply_text(history_text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sorry, I don't understand that command. Type /help for a list of commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Here are the available commands:\n"
        "/start - Start the bot\n"
        "/exchangerate base_currency target_currency - Get the exchange rate between currencies\n"
        "/history - Show your requests history\n"
        "/help - Show this message\n\n"
        "Supported currencies:\n"
    )

    supported_currencies = get_supported_currencies()
    supported_currencies_text = "\n".join(f"{code}: {name}" for code, name in supported_currencies.items())

    await update.message.reply_text(help_text + supported_currencies_text)
