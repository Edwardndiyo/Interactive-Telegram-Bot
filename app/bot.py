# from fastapi import FastAPI
# import telegram
# from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
# import os
# from dotenv import load_dotenv

# app = FastAPI()
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# bot = telegram.Bot(token=TOKEN)

# # Mock database with multi-level categories
# products_db = {
#     "gadgets": {
#         "Smartphones": {
#             "Samsung": [
#                 {"id": 1, "name": "Samsung Galaxy S23", "price": "$1000", "specs": "128GB, 8GB RAM, 5G", "image": "https://example.com/s23.jpg"},
#                 {"id": 2, "name": "Samsung Galaxy A54", "price": "$500", "specs": "128GB, 6GB RAM, 4G", "image": "https://example.com/a54.jpg"},
#             ],
#             "Apple": [
#                 {"id": 3, "name": "iPhone 14 Pro", "price": "$1200", "specs": "256GB, 6GB RAM, iOS", "image": "https://example.com/iphone14pro.jpg"},
#                 {"id": 4, "name": "iPhone SE", "price": "$600", "specs": "64GB, 4GB RAM, iOS", "image": "https://example.com/iphonese.jpg"},
#             ]
#         },
#         "Smartwatches": {
#             "Samsung": [
#                 {"id": 5, "name": "Samsung Galaxy Watch 5", "price": "$350", "specs": "40mm, LTE", "image": "https://example.com/galaxywatch5.jpg"}
#             ],
#             "Apple": [
#                 {"id": 6, "name": "Apple Watch Series 8", "price": "$500", "specs": "GPS, 44mm", "image": "https://example.com/applewatch8.jpg"}
#             ]
#         }
#     }
# }

# # Store user navigation state
# user_state = {}

# async def start(update: Update, context: CallbackContext):
#     """ Display main menu """
#     keyboard = [
#         [InlineKeyboardButton("🔍 Search Product", callback_data="search_product")],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Welcome to the bot! Select an option:", reply_markup=reply_markup)

# async def search_product(update: Update, context: CallbackContext):
#     """ Show top-level product categories """
#     keyboard = [[InlineKeyboardButton("📱 Gadgets", callback_data="category_gadgets")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text("Select a category:", reply_markup=reply_markup)

# async def handle_category_selection(update: Update, context: CallbackContext):
#     """ Handle main category selection (e.g., Gadgets) """
#     query = update.callback_query
#     category = query.data.split("_")[1]

#     # Store user's navigation history
#     user_state[query.message.chat_id] = {"path": [category]}

#     # Get subcategories (e.g., Smartphones, Smartwatches)
#     subcategories = products_db[category].keys()
#     keyboard = [[InlineKeyboardButton(f"{sub}", callback_data=f"subcategory_{sub}")] for sub in subcategories]
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])
    
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await query.message.reply_text("Select a subcategory:", reply_markup=reply_markup)

# async def handle_subcategory_selection(update: Update, context: CallbackContext):
#     """ Handle subcategory selection (e.g., Smartphones) """
#     query = update.callback_query
#     subcategory = query.data.split("_")[1]
    
#     user_id = query.message.chat_id
#     user_state[user_id]["path"].append(subcategory)

#     # Get available brands
#     brands = products_db["gadgets"][subcategory].keys()
#     keyboard = [[InlineKeyboardButton(brand, callback_data=f"brand_{brand}")] for brand in brands]
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await query.message.reply_text(f"Select a brand for {subcategory}:", reply_markup=reply_markup)

# async def handle_brand_selection(update: Update, context: CallbackContext):
#     """ Handle brand selection (e.g., Samsung, Apple) """
#     query = update.callback_query
#     brand = query.data.split("_")[1]

#     user_id = query.message.chat_id
#     user_state[user_id]["path"].append(brand)

#     # Get available models
#     category, subcategory = user_state[user_id]["path"][:2]
#     models = products_db[category][subcategory][brand]

#     keyboard = [[InlineKeyboardButton(model["name"], callback_data=f"model_{model['id']}")] for model in models]
#     keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])

#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await query.message.reply_text(f"Select a model from {brand}:", reply_markup=reply_markup)

# async def handle_model_selection(update: Update, context: CallbackContext):
#     """ Display selected product details """
#     query = update.callback_query
#     model_id = int(query.data.split("_")[1])

#     user_id = query.message.chat_id
#     category, subcategory, brand = user_state[user_id]["path"][:3]
    
#     # Find the selected product
#     selected_product = next((p for p in products_db[category][subcategory][brand] if p["id"] == model_id), None)
#     if selected_product:
#         message = f"📌 *{selected_product['name']}*\n💰 Price: {selected_product['price']}\n🛠 Specs: {selected_product['specs']}"
#         keyboard = [[InlineKeyboardButton("🛒 Order Now", callback_data=f"order_{model_id}")]]
#         keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back")])
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         await context.bot.send_photo(
#             chat_id=user_id,
#             photo=selected_product["image"],
#             caption=message,
#             parse_mode="Markdown",
#             reply_markup=reply_markup
#         )

# async def handle_back(update: Update, context: CallbackContext):
#     """ Handle back navigation """
#     query = update.callback_query
#     user_id = query.message.chat_id

#     if user_id in user_state and user_state[user_id]["path"]:
#         user_state[user_id]["path"].pop()  # Remove last selection

#         if not user_state[user_id]["path"]:  
#             await search_product(update, context)  # Go back to category selection
#         else:
#             last_step = user_state[user_id]["path"][-1]

#             if last_step in products_db["gadgets"]:
#                 await handle_category_selection(update, context)
#             elif last_step in ["Smartphones", "Smartwatches"]:
#                 await handle_subcategory_selection(update, context)
#             else:
#                 await handle_brand_selection(update, context)
#     else:
#         await start(update, context)  # Default fallback

# # Register handlers
# app = Application.builder().token(TOKEN).build()
# app.add_handler(CommandHandler("start", start))
# app.add_handler(CallbackQueryHandler(search_product, pattern="^search_product$"))
# app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
# app.add_handler(CallbackQueryHandler(handle_subcategory_selection, pattern="^subcategory_"))
# app.add_handler(CallbackQueryHandler(handle_brand_selection, pattern="^brand_"))
# app.add_handler(CallbackQueryHandler(handle_model_selection, pattern="^model_"))
# app.add_handler(CallbackQueryHandler(handle_back, pattern="^back$"))

# if __name__ == "__main__":
#     app.run_polling()


# first implementation before attempting to make it modular up here




from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers.start import start
from handlers.explore import explore_product, explore_handlers  # Import the handler list
from handlers.search import search_product, search_handlers
from handlers.orders import orders_handlers  # Import the orders handlers
from services.authentication import authenticate_user

# Initialize the bot application
app = Application.builder().token(TOKEN).build()

# Register the /start command handler
app.add_handler(CommandHandler("start", start))

# Register the explore_product handler
app.add_handler(CallbackQueryHandler(explore_product, pattern="^explore_product$"))

# Register the search_product handler
app.add_handler(CallbackQueryHandler(search_product, pattern="^search_product$"))


# Register all handlers from explore.py
for handler in explore_handlers:
    app.add_handler(handler)

# Register all handlers from search.py
for handler in search_handlers:
    app.add_handler(handler)

# Register all handlers from orders.py
for handler in orders_handlers:
    app.add_handler(handler)

# Run the bot
if __name__ == "__main__":
    app.run_polling()