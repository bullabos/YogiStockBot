
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

# --- Helper Functions ---

def get_usd_to_inr():
    try:
        url = "https://api.exchangerate.host/latest?base=USD&symbols=INR"
        response = requests.get(url).json()
        return response["rates"]["INR"]
    except:
        return 83.0  # fallback rate

# --- Fetch Functions ---

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano,ripple,dogecoin,tron&vs_currencies=usd"
        response = requests.get(url).json()
        rate = get_usd_to_inr()
        data = (
            f"₿ Bitcoin: ₹{response['bitcoin']['usd'] * rate:,.2f}\n"
            f"Ξ Ethereum: ₹{response['ethereum']['usd'] * rate:,.2f}\n"
            f"◎ Solana: ₹{response['solana']['usd'] * rate:,.2f}\n"
            f"₳ Cardano: ₹{response['cardano']['usd'] * rate:,.2f}\n"
            f"✦ Ripple: ₹{response['ripple']['usd'] * rate:,.2f}\n"
            f"🐶 Dogecoin: ₹{response['dogecoin']['usd'] * rate:,.2f}\n"
            f"⚡ Tron: ₹{response['tron']['usd'] * rate:,.2f}"
        )
        return data
    except:
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
    except:
        return "⚠️ Failed to fetch currency data."

def get_indices_data():
    try:
        symbols = {
            "Nifty 50": "^NSEI",
            "Sensex": "^BSESN",
            "Bank Nifty": "^NSEBANK",
            "Nifty Midcap 100": "^CNXMDCP",
            "Nifty Smallcap 100": "^CNXSMCP",
            "S&P 500": "^GSPC",
            "Nasdaq": "^IXIC",
            "FTSE 100": "^FTSE",
            "CAC 40": "^FCHI",
            "DAX": "^GDAXI",
            "Nikkei 225": "^N225",
            "Hang Seng": "^HSI",
            "KOSPI": "^KS11"
        }
        results = []
        for name, symbol in symbols.items():
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
            r = requests.get(url).json()
            price = r['quoteResponse']['result'][0]['regularMarketPrice']
            results.append(f"📊 {name}: {price}")
        return "\n".join(results)
    except:
        return "⚠️ Failed to fetch indices data."

def get_commodities_data():
    try:
        symbols = {
            "Brent Crude": "BZ=F",
            "Crude Oil": "CL=F",
            "Gold": "GC=F",
            "Silver": "SI=F"
        }
        rate = get_usd_to_inr()
        results = []
        for name, symbol in symbols.items():
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
            r = requests.get(url).json()
            price = r['quoteResponse']['result'][0]['regularMarketPrice']
            results.append(f"🛢 {name}: ₹{price * rate:.2f}")
        return "\n".join(results)
    except:
        return "⚠️ Failed to fetch commodity data."

def get_bonds_data():
    try:
        symbols = {
            "India 10Y": "^IN10Y",
            "US 10Y": "^TNX",
            "Germany 10Y": "^DE10Y",
            "Japan 10Y": "^JP10Y",
            "China 10Y": "^CN10Y"
        }
        results = []
        for name, symbol in symbols.items():
            url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
            r = requests.get(url).json()
            price = r['quoteResponse']['result'][0]['regularMarketPrice']
            results.append(f"💹 {name}: {price}%")
        return "\n".join(results)
    except:
        return "⚠️ Failed to fetch bond data."

# --- Telegram Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi Subhadip 👋\nWelcome to YogiStockBot 📊\nChoose a category 👇",
        reply_markup=keyboard
    )

async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_crypto_data())

async def currencies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_currency_data())

async def indices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_indices_data())

async def commodities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_commodities_data())

async def bonds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_bonds_data())

async def update_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{get_crypto_data()}\n\n{get_currency_data()}"
    await update.message.reply_text(text)

# --- App Run ---

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("crypto", crypto))
app.add_handler(CommandHandler("currencies", currencies))
app.add_handler(CommandHandler("indices", indices))
app.add_handler(CommandHandler("commodities", commodities))
app.add_handler(CommandHandler("bonds", bonds))
app.add_handler(CommandHandler("update", update_all))
app.run_polling()
