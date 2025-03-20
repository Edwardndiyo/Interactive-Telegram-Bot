from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, MessageHandler, filters, CallbackQueryHandler
from app.utils.database import compare_product_db

async def compare_product(update: Update, context: CallbackContext):
    """Prompt the user to enter two product names."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        # Edit the existing message to display the comparison prompt
        await query.edit_message_text(
            "Enter the names of two products separated by a comma.\n\n"
            "Example: iPhone 13, Samsung Galaxy S21\n\n\n\n\n"
            
            

            "OR...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
        )
    else:
        # If triggered by a direct message (e.g., /compare command)
        await update.message.reply_text(
            "Enter the names of two products separated by a comma.\n\n"
            "Example: iPhone 13, Samsung Galaxy S21\n\n\n\n\n"
            
            

            "OR...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
            ])
        )
    # Set the state to wait for product names
    context.user_data["state"] = "compare:awaiting_products"

async def handle_product_input(update: Update, context: CallbackContext):
    """Handle user input of two product names."""
    if context.user_data.get("state") != "compare:awaiting_products":
        return  # Ignore if not in the correct state

    user_input = update.message.text.strip()
    products = [p.strip() for p in user_input.split(",")]

    # Validate input
    if len(products) != 2:
        # Create a "Back to Main Menu" button
        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Invalid input. Please enter exactly two product names separated by a comma.\n\n"
            "Example: iPhone 13, Samsung Galaxy S21\n\n\n"
            "Or, click the button to return to the main menu. ⬇️",
            reply_markup=reply_markup
        )
        return

    product1, product2 = products

    # Make product names case-insensitive by converting to lowercase
    product1_lower = product1.lower()
    product2_lower = product2.lower()

    # Fetch product details (case-insensitive lookup)
    product1_data = None
    product2_data = None

    for product_name, product_info in compare_product_db.items():
        if product_name.lower() == product1_lower:
            product1_data = product_info
        if product_name.lower() == product2_lower:
            product2_data = product_info

    if not product1_data or not product2_data:
        # Create a "Back to Main Menu" button
        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "❌ Sorry, one or both of the products could not be found. Please try again.\n\n\n"
            "Or, click the button to return to the main menu. ⬇️",
            reply_markup=reply_markup
        )
        return

    # Format the comparison result
    comparison_result = (
        "🔍 Comparison Result:\n\n"
        f"📌 {product1}\n"
        f"- Price: {product1_data['price']}\n"
        f"- Features: {product1_data['features']}\n\n"
        f"📌 {product2}\n"
        f"- Price: {product2_data['price']}\n"
        f"- Features: {product2_data['features']}\n\n"
        "🔙 Back to Main Menu"
    )

    # Create buttons for "Request Images" and "Back to Main Menu"
    keyboard = [
        [InlineKeyboardButton("🖼️ Request Images", callback_data=f"request_images:{product1_lower}:{product2_lower}")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(comparison_result, reply_markup=reply_markup)

    # Clear the state
    context.user_data.pop("state", None)

async def handle_request_images(update: Update, context: CallbackContext):
    """Handle the "Request Images" button click."""
    query = update.callback_query
    await query.answer()

    # Extract product names from the callback data
    _, product1, product2 = query.data.split(":")

    # Fetch product details
    product1_data = compare_product_db.get(product1)
    product2_data = compare_product_db.get(product2)

    if not product1_data or not product2_data:
        await query.edit_message_text("❌ Sorry, product details could not be found.")
        return

    # Fetch product images from the database
    product1_image = product1_data.get("image", "https://example.com/default.jpg")
    product2_image = product2_data.get("image", "https://example.com/default.jpg")

    # Send the first product image with description and "Order Now" button
    await query.message.reply_photo(
        photo=product1_image,
        caption=(
            f"📌 {product1}\n"
            f"- Price: {product1_data['price']}\n"
            f"- Features: {product1_data['features']}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Order Now", callback_data=f"order:{product1}")]
        ])
    )

    # Send the second product image with description and "Order Now" button
    await query.message.reply_photo(
        photo=product2_image,
        caption=(
            f"📌 {product2}\n"
            f"- Price: {product2_data['price']}\n"
            f"- Features: {product2_data['features']}"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Order Now", url="https://example.com/order")]
        ])
    )

    # Add a "Back to Main Menu" button
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("You can now return to the main menu.", reply_markup=reply_markup)

async def handle_main_menu(update: Update, context: CallbackContext):
    """Handle the main menu button click."""
    query = update.callback_query
    await query.answer()

    # Clear the state
    context.user_data.pop("state", None)

    # Send a message to the user indicating they are back to the main menu
    await query.edit_message_text(
        "You are now back to the main menu.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Compare Products", callback_data="compare_product")]
        ])
    )

# Register handlers
compare_handlers = [
    CallbackQueryHandler(compare_product, pattern="^compare_product$"),
    CallbackQueryHandler(handle_request_images, pattern="^request_images:"),
    CallbackQueryHandler(handle_main_menu, pattern="^main_menu$"),
]