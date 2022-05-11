"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from email import message
from turtle import update
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('seaborn')
import yfinance as yf

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CallbackContext, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Start function Bot
# 
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name
    await update.message.reply_html(
        rf"Yo {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await context.job_queue.run_repeating(report, interval=3600, first=10, context=name, chat_id=chat_id)   #CREATE JOB

async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""\
Sono Glider, ti aiuterò a guadagnare con le crypto analizzando il mercato ;) \n \
/perc /help \
""")

async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def perc_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
        await update.message.reply_text(cry())

def cry():
    start="2021-01-01"
    end=datetime.today().strftime('%Y-%m-%d')

    buy = 31048.416016   # DA SISTEMARE  --------------------------------------------------------------------------------------------

    stock = ["BTC-USD"]  # DA SISTEMARE -------------------------------------------------------------------------------------------
    for x in stock:
        df_d = yf.download(tickers=x, start=start, end=end, interval="1h")
  
    current = df_d['Close'].iloc[-2]

    def perc(x,y):
        return ((x/y) * 100) -100

    guadagno = perc(current, buy)
    guadagno = (f'{guadagno:.10f}')
    guadagno = guadagno + ' %'
    #print(guadagno)
    return ("Il profitto generato finora è del: \n" + guadagno)

async def report(context: CallbackContext):
    # Send indicator
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"{str(sma())}")
#Create Small moving average sma20 & sma50
def sma():
    start="2021-01-01"
    end=datetime.today().strftime('%Y-%m-%d')
    stock = ["BTC-USD"]          # ---------------------------------------------------------------------------------------------------
    for x in stock:
        df_d = yf.download(tickers=x, start=start, end=end, interval="1d")
    df_d['SMA50'] = df_d['Adj Close'].rolling(window=50).mean()
    df_d['SMA20'] = df_d['Adj Close'].rolling(window=20).mean()
    df_d['trx'] = np.where(df_d['SMA20'] > df_d['SMA50'], True, False)

    
    if df_d['trx'].iloc[-1] == True:
        return "Buy!"
    else:
        return "sell " + str(df_d['SMA20'].iloc[-1])
    


def main() -> None:
    """Start the bot."""

    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5365141816:AAHZJeKg5n_QkBp5klHbucumSgcdCjgaVYA").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("perc", perc_command))
    application.add_handler(CommandHandler("sma", sma))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
