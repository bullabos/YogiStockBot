
import os
import logging
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

keyboard = ReplyKeyboardMarkup(
    [['/crypto', '/currencies'], ['/indices', '/commodities'], ['/bonds', '/update']],
    resize_keyboard=True
)

# --- Real-Time Data Fetch Functions ---

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano,ripple,dogecoin,tron&vs_currencies=usd"
        response = requests.get(url).json()
        data = (
            f"₿ Bitcoin: ${response['bitcoin']['usd']:,}\n"
            f"Ξ Ethereum: ${response['ethereum']['usd']:,}\n"
            f"◎ Solana: ${response['solana']['usd']:,}\n"
            f"₳ Cardano: ${response['cardano']['usd']:,}\n"
            f"✦ Ripple: ${response['ripple']['usd']:,}\n"
            f"🐶 Dogecoin: ${response['dogecoin']['usd']:,}\n"
            f"⚡ Tron: ${response['tron']['usd']:,}"
        )
        return data
    except Exception as e:
        return "⚠️ Failed to fetch crypto data."

def get_currency_data():
    try:
        url = "https://api.exchangerate.host/latest?base=USD&symbols=INR,EUR,GBP,JPY,CNY"
        response = requests.get(url).json()
        rates = response["rates"]
        data = (
            f"💵 USD/INR: ₹{rates['INR']:.2f}\n"
            f"💶 EUR/INR: ₹{rates['INR']/rates['EUR']:.2f}\n"
            f"💷 GBP/INR: ₹{rates['INR']/rates['GBP']:.2f}\n"
            f"💴 JPY/INR: ₹{rates['INR']/rates['JPY']:.2f}\n"
            f"🇨🇳 CNY/INR: ₹{rates['INR']/rates['CNY']:.2f}"
        )
        return data
    except Exception as e:
        return "⚠️ Failed to fetch currency data."

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi Subhadip 👋\nWelcome to YogiStockBot 📊\nChoose a category 👇",
        reply_markup=keyboard
    )

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_crypto_data()
    await update.message.reply_text(data)

async def currencies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_currency_data()
    await update.message.reply_text(data)

async def indices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Indian Indices feature coming soon.")

async def commodities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛢 Commodities feature coming soon.")

async def bonds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📉 Bonds feature coming soon.")

async def update_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Daily market update coming soon.")

# --- Bot Setup ---

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("crypto", crypto))
app.add_handler(CommandHandler("currencies", currencies))
app.add_handler(CommandHandler("indices", indices))
app.add_handler(CommandHandler("commodities", commodities))
app.add_handler(CommandHandler("bonds", bonds))
app.add_handler(CommandHandler("update", update_all))

app.run_polling()
