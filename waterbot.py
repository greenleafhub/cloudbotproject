from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import os
import configparser
import logging
from datetime import date

from pymongo import MongoClient

global mongo1
global db
global collection


def main():
    
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True) #environment
    dispatcher = updater.dispatcher


    global mongo1
    mongo1 = client = MongoClient(os.environ['MONGO_CLIENT'])
    global db
    db = client['project']
    global collection
    collection = db['database']
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("today", today))
    dispatcher.add_handler(CommandHandler("check", check))
    dispatcher.add_handler(CommandHandler("checkpast", checkpast))
 
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(' /add <input ml> to record the amount of water you drank. \n/check to see the amount of water you drank today. \n/checkpast <input integer> to see last <number> of records. \n/today to confirm the date of today.')


def add(update: Update, context: CallbackContext) -> None:
    name = str(update.message.chat_id)  
    todaydate = str(date.today())

    global mongo1            
    global db
    global collection
    
    print(name,todaydate)
    query = ({"name":name, "date":todaydate})
    results_number = collection.count_documents(query)
    results = collection.find(query)

    if results_number == 0:
        print("Creating new record: ", name, todaydate)
        post = {"name": name, "date":todaydate}
        x = collection.insert_one(post)
    else:
        print("Already have result.")
        for result in results:
            print("Existing record: ", result)
    
    try:                   
        logging.info(context.args[0])
        ml = int(context.args[0])   # <-- store the keyword

        query = ({"name":name, "date":todaydate})
        increase = {"$inc":{"amount":ml}}
        y = collection.update_one(query, increase)
        
        update.message.reply_text('You have added ' + str(ml) +  'ml.')
        
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <water amount in integer>')

def today(update: Update, context: CallbackContext) -> None:
    name = str(update.message.from_user.username)   #update.message.chat_id
    todaydate = str(date.today())
    update.message.reply_text('Good day, ' + name + '! Today is ' + str(todaydate))


def check(update: Update, context: CallbackContext) -> None:
    name = str(update.message.chat_id)  
    todaydate = str(date.today())

    global mongo1            
    global db
    global collection
    
    print(name,date)
    query = ({"name":name, "date":todaydate})
    results_number = collection.count_documents(query)
    results = collection.find(query)
    if results_number == 0:
        print("Creating new record: ", name, todaydate)
        post = {"name": name, "date":todaydate, "amount": 0}
        x = collection.insert_one(post)
        update.message.reply_text('Today you haven''t drink any water.')
    else:
        for result in results:
            print("Existing record: ", result)
        cups = int(result["amount"]) // 240
        percentage = cups/8 * 100
        update.message.reply_text('Today you have drank ' + str(result["amount"]) +  'ml, which is around ' + str(cups) + ' cup(s) of water. \nThe daily recommendation is to drink 8 cups a day. You have completed ' + str(percentage) + '% of the recommendation.')
        
    

def checkpast(update: Update, context: CallbackContext) -> None:
    name = str(update.message.chat_id)  

    global mongo1            
    global db
    global collection

    try:                   
        logging.info(context.args[0])
        days = int(context.args[0])   # <-- store the keyword
   
        print(name,date)
        query = ({"name":name})
        results_number = collection.count_documents(query)
        results = collection.find(query)
        if results_number == 0:
            update.message.reply_text('You don''t have any past records. Start recording today!')
        else:
            i = results_number
            for result in results:
                print("Existing record: ", result)
                i = i-1
                if i < days:
                    cups = int(result["amount"]) // 240
                    percentage = cups/8 * 100
                    update.message.reply_text('On '+str(result["date"])+' you have drank ' + str(result["amount"]) +  'ml, which is around ' + str(cups) + ' cup(s) of water. \nThe daily recommendation is to drink 8 cups a day. You have completed ' + str(percentage) + '% of the recommendation.')


    except (IndexError, ValueError):
        update.message.reply_text('Usage: /checkpast <integer> for checking the last <number> of records.')


if __name__ == '__main__':
    main()
