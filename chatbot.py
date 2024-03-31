from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
CallbackContext)
import configparser
import logging
from ChatGPT_HKBU import HKBU_ChatGPT
import api

global redis1

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    global chatgpt
    # You can set this logging module, so you will know when
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    #echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    #dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram

    dispatcher.add_handler(CommandHandler("steambind", steambind))
    dispatcher.add_handler(CommandHandler("steamgame", steamgame))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))

    # dispatcher for chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text = reply_message)
    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

def steambind(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    steamapi = api.Api('steambind_path')
    try:
        response = steamapi.bind_user_info(context.args[0],context.args[1],context.args[2])    
    except (IndexError, ValueError):
        response = update.message.reply_text('Usage: /steambind <userid> <nickname> <steamid>')
    if response == '-1':
        msg = 'Binding error! Nickname already exists.'
    elif response == '-2':
        msg = 'Binding error! Invalid Steam 64-bit ID.'
    else: 
        msg = response
    update.message.reply_text(msg)
    del steamapi

def steamgame(update: Update, context: CallbackContext) -> None:
    steamapi = api.Api('GetsteamRecentlyPlayedGames_path')
    try:
        response = steamapi.GetsteamRecentlyPlayedGames(context.args[0])
    except (IndexError, ValueError):
        response = update.message.reply_text('Usage: /steamgame <nickname>')
    if response == '-1':
        msg = 'Binding error! Nickname already exists.'
    elif response == '-2':
        msg = 'Binding error! Invalid Steam 64-bit ID.'
    else: 
        total_count = str(response['response']['total_count'])
        games = response['response']['games']
        msg = f'{context.args[0]} played a total of {total_count} game(s) in the last two weeks.\n'
        for index,game in enumerate(games):
            name = game['name']
            playtime_forever = game['playtime_2weeks']
            playtime_forever = "{:.2f}".format((playtime_forever / 60))
            msg += f"[{index + 1}]{name}[{playtime_forever}h]\n"
    update.message.reply_text(msg)
    del steamapi

def hello_command(update: Update, context: CallbackContext) -> None:
    try:
        msg = context.args[0]
        update.message.reply_text('Good day, ' + msg)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <someone>')    
 

if __name__ == '__main__':
    main()