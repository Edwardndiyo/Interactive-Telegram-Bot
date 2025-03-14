# import os
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# load_dotenv()
# BOT_TOKEN = os.getenv("BOT_TOKEN")

# async def start(update: Update, context: CallbackContext):
#     await update.message.reply_text("Hello! I am your test bot.")

# async def echo(update: Update, context: CallbackContext):
#     await update.message.reply_text(update.message.text)

# def main():
#     app = Application.builder().token(BOT_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
#     app.run_polling()

# if __name__ == "__main__":
#     main()






# from fastapi import FastAPI
# import telegram
# from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
# import os
# from dotenv import load_dotenv

# app = FastAPI()
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# bot = telegram.Bot(token=TOKEN)

# def main_menu():
#     keyboard = [
#         [InlineKeyboardButton("🔍 Search Product", callback_data="search_product")],
#         [InlineKeyboardButton("📦 Orders (Authenticated)", callback_data="orders")],
#         [InlineKeyboardButton("👤 User Profile (Authenticated)", callback_data="profile")],
#         [InlineKeyboardButton("⚖️ Quick Comparison", callback_data="compare")],
#         [InlineKeyboardButton("🤖 AI Assistant", callback_data="ai_assistant")]
#     ]
#     return InlineKeyboardMarkup(keyboard)

# async def start(update: Update, context: CallbackContext):
#     await update.message.reply_text("Welcome to Deimr Stella! Please select an option:",
#                                     reply_markup=main_menu())

# async def button_handler(update: Update, context: CallbackContext):
#     query = update.callback_query
#     await query.answer()
    
#     if query.data == "search_product":
#         await query.message.reply_text("Please enter the product name you are looking for.")
#     elif query.data == "orders":
#         await query.message.reply_text("🔑 Authentication required for orders.")
#     elif query.data == "profile":
#         await query.message.reply_text("🔑 Authentication required for user profile.")
#     elif query.data == "compare":
#         await query.message.reply_text("Enter two product names separated by a comma for comparison.")
#     elif query.data == "ai_assistant":
#         await query.message.reply_text("🤖 AI Assistant coming soon...")

# application = Application.builder().token(TOKEN).build()
# application.add_handler(CommandHandler("start", start))
# application.add_handler(CallbackQueryHandler(button_handler))

# if __name__ == "__main__":
#     application.run_polling()




from fastapi import FastAPI, Request, Depends
import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import random
import json
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

# Mock Database
users = {}
orders = {}
products = [
    {"id": 1, "name": "Laptop", "price": "$1000"},
    {"id": 2, "name": "Phone", "price": "$500"},
    {"id": 3, "name": "Tablet", "price": "$700"},
]

def generate_otp():
    return str(random.randint(100000, 999999))

# Start Command
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("1️⃣ Search Product 🔍", callback_data="search_product"), InlineKeyboardButton("2️⃣ Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("3️⃣ User Profile 👤", callback_data="profile"), InlineKeyboardButton("4️⃣ Quick Comparison ⚖️", callback_data="compare")]
    ]
    
    # If odd number of options, make the last button full width
    keyboard.append([InlineKeyboardButton("5️⃣ AI Assistant 🤖", callback_data="ai_assistant")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "search_product":
        await search_product(update, context)
    elif query.data == "orders":
        await authenticate(update, context, "orders")
    elif query.data == "profile":
        await authenticate(update, context, "profile")
    elif query.data == "compare":
        await update.callback_query.message.reply_text("Enter two product names separated by a comma.")
    elif query.data == "ai_assistant":
        await update.callback_query.message.reply_text("AI Assistant coming soon...")

async def search_product(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text("Please enter the product name you are looking for.")

async def authenticate(update: Update, context: CallbackContext, section: str):
    user_id = update.callback_query.message.chat_id
    otp = generate_otp()
    users[user_id] = {"otp": otp, "authenticated": False}
    await update.callback_query.message.reply_text(f"An OTP has been sent to your email. Please enter it.")

async def verify_otp(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    otp_entered = update.message.text
    if users.get(user_id, {}).get("otp") == otp_entered:
        users[user_id]["authenticated"] = True
        await update.message.reply_text("✅ Authentication successful! What would you like to do?")
    else:
        await update.message.reply_text("❌ Incorrect OTP. Please try again.")

async def compare_products(update: Update, context: CallbackContext, products_to_compare):
    response = "🔍 Comparison Result:\n"
    for product_name in products_to_compare:
        product = next((p for p in products if product_name.strip().lower() in p['name'].lower()), None)
        if product:
            response += f"📌 {product['name']} - Price: {product['price']}\n"
    await update.message.reply_text(response)

app = Application.builder().token(TOKEN).build()


app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verify_otp))

if __name__ == "__main__":
    app.run_polling()
