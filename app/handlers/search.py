# from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
# from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
# from utils.database import products_db
# from utils.helpers import user_selected_category

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
#         await update.message.reply_text(f"❌ No matching products found in *{category.replace('_', ' ').title()}*. Try another search.")
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

# handler = CallbackQueryHandler(search_product, pattern="^search_product$")
# category_handler = CallbackQueryHandler(handle_category_selection, pattern="^category_")
# search_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query)



from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from utils.database import products_db
from utils.helpers import user_selected_category

async def search_product(update: Update, context: CallbackContext):
    """ Ask user to select a product category first """
    keyboard = [
        [InlineKeyboardButton("🖥️ Gadgets", callback_data="category_gadgets"),
         InlineKeyboardButton("🏠 Home Appliances", callback_data="category_home_appliances")],
        [InlineKeyboardButton("👕 Clothes", callback_data="category_clothes"),
         InlineKeyboardButton("🍕 Food", callback_data="category_food")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Please select a category:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: CallbackContext):
    """ Store selected category and ask for subcategories """
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    category = query.data.split("_")[1]  # Extract category name

    if category not in products_db:
        await query.message.reply_text("❌ Invalid category selected.")
        return

    user_selected_category[user_id] = {"category": category}  # Store selected category

    subcategories = list(products_db[category].keys())  # Get subcategories

    keyboard = [[InlineKeyboardButton(sub.title(), callback_data=f"subcategory_{sub}")] for sub in subcategories]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="search_product")])  # Back button

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"You selected *{category.title()}*. Now, choose a type:", reply_markup=reply_markup)

async def handle_subcategory_selection(update: Update, context: CallbackContext):
    """ Store selected subcategory and ask for brands """
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    subcategory = query.data.split("_")[1]  # Extract subcategory

    user_category = user_selected_category.get(user_id, {}).get("category")

    if not user_category or subcategory not in products_db[user_category]:
        await query.message.reply_text("❌ Invalid subcategory.")
        return

    user_selected_category[user_id]["subcategory"] = subcategory  # Store selected subcategory

    brands = list(products_db[user_category][subcategory].keys())  # Get brands

    keyboard = [[InlineKeyboardButton(brand, callback_data=f"brand_{brand}")] for brand in brands]
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=f"category_{user_category}")])  # Back button

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"You selected *{subcategory.title()}*. Now, choose a brand:", reply_markup=reply_markup)

async def handle_brand_selection(update: Update, context: CallbackContext):
    """ Show products after brand selection """
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    brand = query.data.split("_")[1]  # Extract brand

    user_category = user_selected_category.get(user_id, {}).get("category")
    user_subcategory = user_selected_category.get(user_id, {}).get("subcategory")

    if not user_category or not user_subcategory or brand not in products_db[user_category][user_subcategory]:
        await query.message.reply_text("❌ Invalid brand selection.")
        return

    user_selected_category[user_id]["brand"] = brand  # Store brand

    products = products_db[user_category][user_subcategory][brand][:4]  # Get top 4 products

    if not products:
        await query.message.reply_text(f"❌ No products found for {brand}.")
        return

    for product in products:
        message = f"📌 *{product['name']}*\n💰 Price: {product['price']}\n🛠 Specs: {product['specs']}"
        keyboard = [[InlineKeyboardButton("🛒 Order Now", callback_data=f"order_{product['id']}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_photo(
            chat_id=user_id,
            photo=product["image"],
            caption=message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # Show back button to brand selection
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"subcategory_{user_subcategory}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Go back?", reply_markup=reply_markup)

# category_handler = CallbackQueryHandler(handle_category_selection, pattern="^category_")
# subcategory_handler = CallbackQueryHandler(handle_subcategory_selection, pattern="^subcategory_")
# brand_handler = CallbackQueryHandler(handle_brand_selection, pattern="^brand_")
# Remove dispatcher.add_handler(...)
# Instead, define the handlers and return them as a list

search_handlers = [
    CallbackQueryHandler(handle_category_selection, pattern="^category_"),
    CallbackQueryHandler(handle_subcategory_selection, pattern="^subcategory_"),
    CallbackQueryHandler(handle_brand_selection, pattern="^brand_"),
]

