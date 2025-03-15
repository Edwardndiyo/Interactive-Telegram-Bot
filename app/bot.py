# from fastapi import FastAPI
# import telegram
# from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
# import random
# import json
# import os
# from dotenv import load_dotenv

# app = FastAPI()
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# bot = telegram.Bot(token=TOKEN)

# # Mock Database for Products
# products_db = {
#     "home_appliances": [
#         {"id": 1, "name": "Air Conditioner", "price": "$300", "specs": "1.5HP, Inverter Technology", "image": "https://example.com/ac.jpg"},
#         {"id": 2, "name": "Refrigerator", "price": "$500", "specs": "250L, Double Door", "image": "https://example.com/fridge.jpg"},
#     ],
#     "clothes": [
#         {"id": 3, "name": "Men’s Suit", "price": "$120", "specs": "Slim Fit, Black", "image": "https://example.com/suit.jpg"},
#         {"id": 4, "name": "Women’s Dress", "price": "$80", "specs": "Evening Gown, Red", "image": "https://example.com/dress.jpg"},
#     ],
#     "gadgets": [
#         {"id": 5, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 6, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 7, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 8, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 9, "name": "Wireless Earbuds", "price": "$150", "specs": "Noise Cancelling, Bluetooth 5.0", "image": "https://example.com/earbuds.jpg"},
#     ],
#     "food": [
#         {"id": 10, "name": "Pizza", "price": "$10", "specs": "Pepperoni, Large Size", "image": "https://example.com/pizza.jpg"},
#         {"id": 11, "name": "Burger", "price": "$5", "specs": "Cheese, Beef Patty", "image": "https://example.com/burger.jpg"},
#     ],
# }
# users = {
#     # Example: "user_id": {"email": "test@example.com", "authenticated": False, "otp": None}
# }

# # Store users' selected categories before search
# user_selected_category = {}

# async def start(update: Update, context: CallbackContext):
#     """ Display main menu with options """
#     keyboard = [
#         [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
#          InlineKeyboardButton("Orders 📦", callback_data="orders")],
#         [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
#          InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare")],
#         [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

# async def search_product(update: Update, context: CallbackContext):
#     """ Ask user to select a product category first """
#     keyboard = [
#         [InlineKeyboardButton(" Home Appliances", callback_data="category_home_appliances"),
#          InlineKeyboardButton(" Clothes", callback_data="category_clothes")],
#         [InlineKeyboardButton(" Gadgets", callback_data="category_gadgets"),
#          InlineKeyboardButton(" Food", callback_data="category_food")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text("Please select a category:", reply_markup=reply_markup)

# async def handle_category_selection(update: Update, context: CallbackContext):
#     """ Store selected category and ask for search query """
#     query = update.callback_query
#     await query.answer()

#     user_id = query.message.chat_id
#     category = query.data.split("_")[1]  # Extract category name

#     user_selected_category[user_id] = category  # Store selected category
#     await query.message.reply_text(f"You selected *{category.replace('_', ' ').title()}*.\n\nNow, please enter the product name you're looking for.", parse_mode="Markdown")

# async def handle_search_query(update: Update, context: CallbackContext):
#     """ Search within selected category and return results """
#     user_id = update.message.chat_id
#     query_text = update.message.text.lower()

#     if user_id not in user_selected_category:
#         await update.message.reply_text("❌ Please select a category first by clicking 'Search Product 🔍'.")
#         return

#     category = user_selected_category[user_id]
#     matching_products = [p for p in products_db[category] if query_text in p["name"].lower()]

#     if not matching_products:
#         await update.message.reply_text(f"❌ No matching products found in *{category.replace('_', ' ').title()}*.")
#         return

#     for product in matching_products:
#         message = f"📌 *{product['name']}*\n💰 Price: {product['price']}\n🛠 Specs: {product['specs']}"
#         keyboard = [[InlineKeyboardButton("🛒 Order Now", callback_data=f"order_{product['id']}")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         await context.bot.send_photo(
#             chat_id=update.message.chat_id,
#             photo=product["image"],
#             caption=message,
#             parse_mode="Markdown",
#             reply_markup=reply_markup
#         )

# async def button_handler(update: Update, context: CallbackContext):
#     """ Handle menu button clicks """
#     query = update.callback_query
#     await query.answer()

#     if query.data == "search_product":
#         await search_product(update, context)
#     elif query.data.startswith("category_"):
#         await handle_category_selection(update, context)
#     elif query.data == "orders":
#         await check_authentication(update, context, "orders")
#     elif query.data == "profile":
#         await check_authentication(update, context, "profile")
#     elif query.data == "compare":
#         await query.message.reply_text("Enter two product names separated by a comma.")
#     elif query.data == "ai_assistant":
#         await query.message.reply_text("AI Assistant coming soon...")

# async def check_authentication(update: Update, context: CallbackContext, section: str):
#     """ Check if user is authenticated; if not, ask for email """
#     user_id = update.callback_query.message.chat_id
#     if users.get(user_id, {}).get("authenticated"):
#         await update.callback_query.message.reply_text(f"✅ You are authenticated! Accessing {section}...")
#     else:
#         users[user_id] = {"authenticated": True}
#         await update.callback_query.message.reply_text("Please enter your email to continue.")

# app = Application.builder().token(TOKEN).build()
# app.add_handler(CommandHandler("start", start))
# app.add_handler(CallbackQueryHandler(button_handler))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query))  # Handle product searches

# if __name__ == "__main__":
#     app.run_polling()






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






# from fastapi import FastAPI
# import telegram
# from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
# import os
# from dotenv import load_dotenv

# app = FastAPI()
# load_dotenv()
# TOKEN = os.getenv("BOT_TOKEN")
# bot = telegram.Bot(token=TOKEN)

# # Mock Database for Products
# products_db = {
#     "home_appliances": [
#         {"id": 1, "name": "Air Conditioner", "price": "$300", "specs": "1.5HP, Inverter Technology", "image": "https://example.com/ac.jpg"},
#         {"id": 2, "name": "Refrigerator", "price": "$500", "specs": "250L, Double Door", "image": "https://example.com/fridge.jpg"},
#     ],
#     "clothes": [
#         {"id": 3, "name": "Men’s Suit", "price": "$120", "specs": "Slim Fit, Black", "image": "https://example.com/suit.jpg"},
#         {"id": 4, "name": "Women’s Dress", "price": "$80", "specs": "Evening Gown, Red", "image": "https://example.com/dress.jpg"},
#     ],
#     "gadgets": [
#         {"id": 5, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 6, "name": "Wireless Earbuds", "price": "$150", "specs": "Noise Cancelling, Bluetooth 5.0", "image": "https://example.com/earbuds.jpg"},
#         {"id": 7, "name": "Smart Watch", "price": "$200", "specs": "Waterproof, Heart Rate Monitor", "image": "https://example.com/watch.jpg"},
#     ],
#     "food": [
#         {"id": 8, "name": "Pizza", "price": "$10", "specs": "Pepperoni, Large Size", "image": "https://example.com/pizza.jpg"},
#         {"id": 9, "name": "Burger", "price": "$5", "specs": "Cheese, Beef Patty", "image": "https://example.com/burger.jpg"},
#     ],
# }

# users = {}
# user_selected_category = {}

# async def start(update: Update, context: CallbackContext):
#     """ Display main menu with options """
#     keyboard = [
#         [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
#          InlineKeyboardButton("Orders 📦", callback_data="orders")],
#         [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
#          InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare")],
#         [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

# async def search_product(update: Update, context: CallbackContext):
#     """ Ask user to select a product category first """
#     keyboard = [
#         [InlineKeyboardButton(" Home Appliances", callback_data="category_home_appliances"),
#          InlineKeyboardButton(" Clothes", callback_data="category_clothes")],
#         [InlineKeyboardButton(" Gadgets", callback_data="category_gadgets"),
#          InlineKeyboardButton(" Food", callback_data="category_food")],
#         [InlineKeyboardButton("🔙 Back", callback_data="back_main_menu")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.callback_query.message.reply_text("Please select a category:", reply_markup=reply_markup)

# async def handle_category_selection(update: Update, context: CallbackContext):
#     """ Store selected category and ask for search query """
#     query = update.callback_query
#     await query.answer()

#     user_id = query.message.chat_id
#     category = query.data.split("_")[1]  # Extract category name

#     user_selected_category[user_id] = category  # Store selected category
#     await query.message.reply_text(
#         f"You selected *{category.replace('_', ' ').title()}*.\n\nNow, please enter the product name you're looking for.",
#         parse_mode="Markdown"
#     )

# async def handle_search_query(update: Update, context: CallbackContext):
#     """ Search within selected category and return results """
#     user_id = update.message.chat_id
#     query_text = update.message.text.lower()

#     if user_id not in user_selected_category:
#         await update.message.reply_text("❌ Please select a category first by clicking 'Search Product 🔍'.")
#         return

#     category = user_selected_category[user_id]
#     matching_products = [p for p in products_db[category] if query_text in p["name"].lower()]

#     if not matching_products:
#         keyboard = [[InlineKeyboardButton("🔙 Back to Categories", callback_data="search_product")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await update.message.reply_text(f"❌ No matching products found in *{category.replace('_', ' ').title()}*.", reply_markup=reply_markup)
#         return

#     for product in matching_products:
#         message = f"📌 *{product['name']}*\n💰 Price: {product['price']}\n🛠 Specs: {product['specs']}"
#         keyboard = [
#             [InlineKeyboardButton("🛒 Order Now", callback_data=f"order_{product['id']}")],
#             [InlineKeyboardButton("🔙 Back to Categories", callback_data="search_product")]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)

#         await context.bot.send_photo(
#             chat_id=update.message.chat_id,
#             photo=product["image"],
#             caption=message,
#             parse_mode="Markdown",
#             reply_markup=reply_markup
#         )

# async def button_handler(update: Update, context: CallbackContext):
#     """ Handle menu button clicks """
#     query = update.callback_query
#     await query.answer()

#     if query.data == "search_product":
#         await search_product(update, context)
#     elif query.data.startswith("category_"):
#         await handle_category_selection(update, context)
#     elif query.data == "orders":
#         await check_authentication(update, context, "orders")
#     elif query.data == "profile":
#         await check_authentication(update, context, "profile")
#     elif query.data == "compare":
#         await query.message.reply_text("Enter two product names separated by a comma.")
#     elif query.data == "ai_assistant":
#         await query.message.reply_text("AI Assistant coming soon...")
#     elif query.data == "back_main_menu":
#         await start(update, context)

# async def check_authentication(update: Update, context: CallbackContext, section: str):
#     """ Check if user is authenticated; if not, ask for email """
#     user_id = update.callback_query.message.chat_id
#     if users.get(user_id, {}).get("authenticated"):
#         await update.callback_query.message.reply_text(f"✅ You are authenticated! Accessing {section}...")
#     else:
#         users[user_id] = {"authenticated": True}
#         await update.callback_query.message.reply_text("Please enter your email to continue.")

# app = Application.builder().token(TOKEN).build()
# app.add_handler(CommandHandler("start", start))
# app.add_handler(CallbackQueryHandler(button_handler))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query))

# if __name__ == "__main__":
#     app.run_polling()




# from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
# from config import TOKEN
# from handlers.start import start
# from handlers.search import search_product, handle_category_selection, handle_search_query
# from app.services.authentication import authenticate_user

# app = Application.builder().token(TOKEN).build()

# app.add_handler(CommandHandler("start", start))
# app.add_handler(CallbackQueryHandler(search_product, pattern="^search_product$"))
# app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query))

# if __name__ == "__main__":
#     app.run_polling()





from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TOKEN
from handlers.start import start
from handlers.search import search_product, search_handlers  # Import the handler list
from services.authentication import authenticate_user

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(search_product, pattern="^search_product$"))

# Register all handlers from search.py
for handler in search_handlers:
    app.add_handler(handler)

if __name__ == "__main__":
    app.run_polling()
