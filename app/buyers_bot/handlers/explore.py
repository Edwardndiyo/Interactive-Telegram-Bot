from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from app.utils.database import products_db
from .start import start

def chunk_buttons(buttons, row_size=2):
    """Split buttons into rows of specified size."""
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

user_selected_category = {}

# Step 1: User Initiates Search
async def explore_product(update: Update, context: CallbackContext):
    """Ask user to select a product category."""
    buttons = [
        InlineKeyboardButton("🖥️ Gadgets", callback_data="category_gadgets"),
        InlineKeyboardButton("🏠 Home Appliances", callback_data="category_home_appliances"),
        InlineKeyboardButton("👕 Clothes", callback_data="category_clothes"),
        InlineKeyboardButton("🍕 Food", callback_data="category_food"),
        InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")  # Correct callback data
    ]
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Please select a category:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Please select a category:", reply_markup=reply_markup)


# Step 2: User Selects a Category
async def handle_category_selection(update: Update, context: CallbackContext):
    """Store selected category and ask for subcategories."""
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    category = "_".join(query.data.split("_")[1:])  # Extracts "home_appliances"

    if category not in products_db:
        await query.edit_message_text("❌ Invalid category selected.")
        return

    # Store selected category
    user_selected_category[user_id] = {"category": category, "selection_path": [category]}

    # Get subcategories for the selected category
    subcategories = list(products_db[category].keys())

    # Create buttons for subcategories
    buttons = [InlineKeyboardButton(sub.title(), callback_data=f"subcategory_{sub}") for sub in subcategories]
    buttons.append(InlineKeyboardButton("🔙 Back", callback_data="explore_product"))
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    selection_path = " → ".join(user_selected_category[user_id]["selection_path"])
    await query.edit_message_text(f"🏷️ You’ve selected → {selection_path}\n\nNow, choose a type:", reply_markup=reply_markup)

# Step 3: User Selects a Subcategory
async def handle_subcategory_selection(update: Update, context: CallbackContext):
    """Store selected subcategory and ask for brands."""
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    subcategory = query.data.split("_")[1]  # Extract subcategory

    # Retrieve user's selected category
    user_category = user_selected_category.get(user_id, {}).get("category")

    if not user_category or subcategory not in products_db[user_category]:
        await query.edit_message_text("❌ Invalid subcategory.")
        return

    # Store selected subcategory
    user_selected_category[user_id]["subcategory"] = subcategory
    user_selected_category[user_id]["selection_path"].append(subcategory)

    # Get brands for the selected subcategory
    brands = list(products_db[user_category][subcategory].keys())

    # Create buttons for brands
    buttons = [InlineKeyboardButton(brand, callback_data=f"brand_{brand}") for brand in brands]
    buttons.append(InlineKeyboardButton("🔙 Back", callback_data=f"category_{user_category}"))
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    selection_path = " → ".join(user_selected_category[user_id]["selection_path"])
    await query.edit_message_text(f"🏷️ You’ve selected → {selection_path}\n\nNow, choose a brand:", reply_markup=reply_markup)

# Step 4: User Selects a Brand
async def handle_brand_selection(update: Update, context: CallbackContext):
    """Show products after brand selection."""
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id
    brand = query.data.split("_")[1]  # Extract brand

    # Retrieve user's selected category and subcategory
    user_category = user_selected_category.get(user_id, {}).get("category")
    user_subcategory = user_selected_category.get(user_id, {}).get("subcategory")

    if not user_category or not user_subcategory or brand not in products_db[user_category][user_subcategory]:
        await query.edit_message_text("❌ Invalid brand selection.")
        return

    # Store selected brand
    user_selected_category[user_id]["brand"] = brand
    user_selected_category[user_id]["selection_path"].append(brand)

    # Get top 4 products for the selected brand
    products = products_db[user_category][user_subcategory][brand][:4]

    if not products:
        await query.edit_message_text(f"❌ No products found for {brand}.")
        return

    # Store product message IDs for later deletion
    product_message_ids = []

    # Display each product with image, name, price, and specs
    for product in products:
        message = (
            f"📌 *{product['name']}*\n"
            f"💰 Price: {product['price']}\n"
            f"🛠 Specs: {product['specs']}"
        )
        keyboard = [[InlineKeyboardButton("🛒 Order Now", callback_data=f"order_{product['id']}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        sent_message = await context.bot.send_photo(
            chat_id=user_id,
            photo=product["image"],
            caption=message,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        product_message_ids.append(sent_message.message_id)

    # Store product message IDs in user_data
    context.user_data["product_message_ids"] = product_message_ids

    # Add a back button at the end of the product list
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data=f"subcategory_{user_subcategory}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    back_message = await query.message.reply_text("Go back?", reply_markup=reply_markup)

    # Store the back button message ID for later deletion
    context.user_data["back_message_id"] = back_message.message_id


async def handle_back_from_products(update: Update, context: CallbackContext):
    """Handle back navigation from product display."""
    query = update.callback_query
    await query.answer()

    user_id = query.message.chat_id

    # Delete product messages
    product_message_ids = context.user_data.get("product_message_ids", [])
    for message_id in product_message_ids:
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=message_id)
        except Exception as e:
            print(f"Failed to delete message {message_id}: {e}")

    # Delete the back button message
    back_message_id = context.user_data.get("back_message_id")
    if back_message_id:
        try:
            await context.bot.delete_message(chat_id=user_id, message_id=back_message_id)
        except Exception as e:
            print(f"Failed to delete back button message {back_message_id}: {e}")

    # Clear stored message IDs
    context.user_data.pop("product_message_ids", None)
    context.user_data.pop("back_message_id", None)

    # Return to the previous menu
    await handle_subcategory_selection(update, context)


# Step 5: Order Process (Placeholder)
async def handle_order(update: Update, context: CallbackContext):
    """Handle order placement."""
    query = update.callback_query
    await query.answer()

    product_id = query.data.split("_")[1]  # Extract product ID
    await query.edit_message_text(f"✅ Order placed for product ID: {product_id}!")

# Register handlers
\

explore_handlers = [
    CallbackQueryHandler(handle_category_selection, pattern="^category_"),
    CallbackQueryHandler(handle_subcategory_selection, pattern="^subcategory_"),
    CallbackQueryHandler(handle_brand_selection, pattern="^brand_"),
    CallbackQueryHandler(handle_order, pattern="^order_"),
    CallbackQueryHandler(start, pattern="^main_menu$"),  # Handle "Back to Main Menu"
    CallbackQueryHandler(handle_back_from_products, pattern="^subcategory_"),  # Handle "Back" from products
]