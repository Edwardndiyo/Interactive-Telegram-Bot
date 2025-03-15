from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters

# Mock function to fetch matching products (replace with actual database query)
def fetch_matching_products(product_name: str):
    """Simulate fetching top 3 matching products."""
    return [
        {"name": "Product 1", "image": "https://example.com/product1.jpg", "price": "$50", "details": "Color: Red, Size: M"},
        {"name": "Product 2", "image": "https://example.com/product2.jpg", "price": "$60", "details": "Color: Blue, Size: L"},
        {"name": "Product 3", "image": "https://example.com/product3.jpg", "price": "$70", "details": "Color: Green, Size: S"},
    ]

async def search_product(update: Update, context: CallbackContext):
    """Step 1: Ask the user to enter the product name."""
    await update.message.reply_text("🔍 Please enter the product name you are looking for.")

    # Set the state to wait for the product name
    context.user_data["state"] = "awaiting_product_name"

async def handle_product_name(update: Update, context: CallbackContext):
    """Step 2: Handle the product name input and display top 3 results."""
    # Check if the current state is "awaiting_product_name"
    if context.user_data.get("state") != "awaiting_product_name":
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

    # Display the top 3 results with images and buttons
    response_text = "Here are the top results for your search:\n\n"
    buttons = []

    for i, product in enumerate(matching_products):
        response_text += f"{i + 1}️⃣ {product['name']} 🖼️\n"
        buttons.append(InlineKeyboardButton(f"{i + 1}️⃣", callback_data=f"product_{i + 1}"))

    # Add "Search Again" and "Back to Main Menu" buttons
    buttons.append(InlineKeyboardButton("🔄 5️⃣ Search Again", callback_data="search_again"))
    buttons.append(InlineKeyboardButton("🏠 6️⃣ Back to Main Menu", callback_data="main_menu"))

    # Chunk buttons into rows of 2
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the response with images (Telegram supports sending images with captions)
    for i, product in enumerate(matching_products):
        await update.message.reply_photo(
            photo=product["image"],
            caption=f"{i + 1}️⃣ {product['name']}"
        )

    await update.message.reply_text(response_text, reply_markup=reply_markup)

    # Set the state to wait for product selection
    context.user_data["state"] = "awaiting_product_selection"
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
        # Return to the main menu
        await show_main_menu(update, context)
    else:
        # Extract the selected product index
        product_index = int(user_choice.split("_")[-1]) - 1
        matching_products = context.user_data.get("matching_products")

        if not matching_products or product_index >= len(matching_products):
            await query.edit_message_text("❌ Invalid selection. Please try again.")
            return

        # Proceed to Step 5: Display product details
        selected_product = matching_products[product_index]
        await display_product_details(update, context, selected_product)

async def display_product_details(update: Update, context: CallbackContext, product: dict):
    """Step 5: Display the selected product's details."""
    query = update.callback_query

    # Prepare the response text
    response_text = (
        f"📌 {product['name']} 🖼️🖼️🖼️\n\n"
        f"💰 Price: {product['price']}\n"
        f"📜 Attributes: {product['details']}\n\n"
    )

    # Add an "Order Product" button (link to the website)
    keyboard = [
        [InlineKeyboardButton("🛒 Order Product", url="https://example.com/order")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the product images (if available)
    await query.message.reply_photo(
        photo=product["image"],
        caption=response_text,
        reply_markup=reply_markup
    )

async def show_main_menu(update: Update, context: CallbackContext):
    """Return to the main menu."""
    # Replace this with your actual main menu implementation
    await update.message.reply_text("🏠 Welcome to the main menu!")

# Register handlers
search_handlers = [
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_name),  # No pattern argument
    CallbackQueryHandler(handle_product_selection, pattern="^product_|search_again|main_menu$"),
]