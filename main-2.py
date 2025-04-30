
import os
import openai
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# === CONFIG ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# === LOGGING ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === PROMPT GENERATOR ===
def build_prompt(theme):
    return f"""
You're a hyper-creative AI that invents absurd, whimsical and cartoonish memecoins as if they belonged in the universe of The Fairly OddParents. Based on the theme "{theme}", generate:

1. A funny, made-up name for the memecoin
2. A 4-letter ticker (like $POOF or $ZUCK)
3. A silly, exaggerated backstory (lore) in 2-3 lines
4. A viral-style tweet to promote the coin

Use the show's tone: unpredictable, fun, childlike but witty.
Return it as a clear list (Name, Ticker, Lore, Tweet).
"""

# === GPT FUNCTION ===
def generate_memecoin(theme):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You create absurd cartoonish crypto coins in the tone of The Fairly OddParents."},
            {"role": "user", "content": build_prompt(theme)}
        ]
    )
    return response['choices'][0]['message']['content']

# === MESSAGE HANDLER ===
def handle_message(update: Update, context: CallbackContext):
    theme = update.message.text
    update.message.reply_text("🎩 TimmyStacks sta creando il tuo coin... aspetta un attimo! 🧪✨")
    try:
        result = generate_memecoin(theme)
        update.message.reply_text(result)
    except Exception as e:
        update.message.reply_text("Oops! Qualcosa è andato storto.")
        print("GPT ERROR:", e)

# === MAIN ===
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
