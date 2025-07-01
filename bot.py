
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

keyboard = ReplyKeyboardMarkup(
    [['/indices', '/crypto'], ['/commodities', '/currencies'], ['/bonds', '/update']],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi Subhadip 👋\nWelcome to YogiStockBot 📊\nChoose a category 👇",
        reply_markup=keyboard
    )

async def indices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇮🇳 Nifty 50: ₹23,541.50\n🇮🇳 Sensex: ₹78,965.30")

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("₿ Bitcoin: $66,000\nΞ Ethereum: $3,400")

async def commodities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛢 Crude Oil: $82.50\n🥇 Gold: $2,350")

async def currencies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💵 USD/INR: ₹83.10\n💷 GBP/INR: ₹106.55")

async def bonds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇮🇳 India 10Y: 7.12%\n🇺🇸 US 10Y: 4.25%")

async def update_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Full Market Update Sent!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("indices", indices))
app.add_handler(CommandHandler("crypto", crypto))
app.add_handler(CommandHandler("commodities", commodities))
app.add_handler(CommandHandler("currencies", currencies))
app.add_handler(CommandHandler("bonds", bonds))
app.add_handler(CommandHandler("update", update_all))

app.run_polling()
