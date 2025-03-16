from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from handlers.start import start  # Import the start function
from utils.database import fetch_matching_products


async def search_product(update: Update, context: CallbackContext):
    """Step 1: Ask the user to enter the product name."""
    if update.callback_query:
        # If triggered by a button click, use the callback query's message
        message = update.callback_query.message
    else:
        # If triggered by a direct message, use the message directly
        message = update.message

    await message.reply_text("🔍 Please enter the product name you are looking for.")

    # Set the state to wait for the product name
    context.user_data["state"] = "search:awaiting_product_name"


async def handle_product_name(update: Update, context: CallbackContext):
    """Step 2: Handle the product name input and display top 3 results."""
    # Check if the current state is "awaiting_product_name"
    if context.user_data.get("state") != "search:awaiting_product_name":
        return  # Ignore if not in the correct state

    product_name = update.message.text

    # Fetch top 3 matching products
    matching_products = fetch_matching_products(product_name)

    if not matching_products:
        await update.message.reply_text(
            "❌ No products found. Please try again with a different name.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Search Again", callback_data="search_again")],
                [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu")],
            ])
        )
        return

    # Display the top 3 results with product names as buttons
    response_text = "Here are the top results for your search:\n\n"
    buttons = []

    for product in matching_products:
        # Add a button for each product with its name
        buttons.append(InlineKeyboardButton(product["name"], callback_data=f"product_{product['id']}"))

    # Add "Search Again" and "Back to Main Menu" buttons
    buttons.append(InlineKeyboardButton("🔄 Search Again", callback_data="search_again"))
    buttons.append(InlineKeyboardButton("🏠 Back to Main Menu", callback_data="main_menu"))

    # Chunk buttons into rows of 2
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the response text with buttons
    await update.message.reply_text(response_text, reply_markup=reply_markup)

    # Set the state to wait for product selection
    context.user_data["state"] = "search:awaiting_product_selection"
    context.user_data["matching_products"] = matching_products


async def handle_product_selection(update: Update, context: CallbackContext):
    """Step 4: Handle the user's selection of a product."""
    query = update.callback_query
    await query.answer()

    user_choice = query.data

    if user_choice == "search_again":
        # Repeat Step 1
        await search_product(update, context)
    elif user_choice == "main_menu":
        # Return to the main menu by calling the start function
        await start(update, context)
    else:
        # Extract the selected product ID
        product_id = user_choice.split("_")[-1]
        matching_products = context.user_data.get("matching_products")

        # Find the selected product
        selected_product = next((p for p in matching_products if p["id"] == product_id), None)

        if not selected_product:
            await query.edit_message_text("❌ Invalid selection. Please try again.")
            return

        # Proceed to Step 5: Display product details
        await display_product_details(update, context, selected_product)



async def display_product_details(update: Update, context: CallbackContext, product: dict):
    """Step 5: Display the selected product's details."""
    query = update.callback_query
    await query.answer()

    # Prepare the response text
    response_text = (
        f"📌 {product['name']} 🖼️🖼️🖼️\n\n"
        f"💰 Price: {product['price']}\n"
        f"📜 Attributes: {product['details']}\n\n"
    )

    # Send the product images (if available) with the details as a standalone message
    await query.message.reply_photo(
        photo=product["image"],
        caption=response_text
    )

    # Add an "Order {Product Name}" button (link to the website)
    keyboard = [
        [InlineKeyboardButton(f"🛒 Order {product['name']}", url="https://example.com/order")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the buttons as a separate message
    await query.message.reply_text("What would you like to do next?", reply_markup=reply_markup)


# Register handlers
search_handlers = [
    # MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_name),  # No pattern argument
    CallbackQueryHandler(handle_product_selection, pattern="^product_|search_again|main_menu$"),
]