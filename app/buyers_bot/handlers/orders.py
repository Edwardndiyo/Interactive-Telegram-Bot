from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime, timedelta
from app.utils.database import users_db

from app.services.authentication import start_authentication,  handle_otp_input, handle_email_input

# Store authentication status (user_id: expiry_time)
# authenticated_users = {}

# Helper function to chunk buttons into rows of 2
def chunk_buttons(buttons, row_size=2):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

# Step 1: Start Orders Flow
# async def start_orders(update: Update, context: CallbackContext):
#     """Prompt user to enter their email."""
#     if update.callback_query:
#         query = update.callback_query
#         await query.answer()
#         message = query.message
#     else:
#         message = update.message

#     await message.reply_text("Please enter your registered email address:")

#     # Set the state to wait for email
#     context.user_data["state"] = "orders:awaiting_email"

# # Step 2: Handle Email Input
# async def handle_email(update: Update, context: CallbackContext):
#     """Handle email input."""
#     if context.user_data.get("state") != "orders:awaiting_email":
#         return  # Ignore if not in the correct state

#     email = update.message.text.strip().lower()
#     print(f"User entered email: {email}")  # Debugging: Print the entered email

#     # Look up the email in the database
#     user_data = users_db.get(email)
#     print(f"User data found: {user_data}")  # Debugging: Print the user data

#     if user_data is not None:  # Explicitly check if user_data is not None
#         # Greet the user and send OTP
#         context.user_data["email"] = email
#         context.user_data["name"] = user_data["name"]
#         await update.message.reply_text(
#             f"Welcome {user_data['name']}, we have sent an OTP to your email. Please provide it here."
#         )

#         # Set the state to wait for OTP
#         context.user_data["state"] = "orders:awaiting_otp"
#     else:
#         # Prompt the user to register
#         keyboard = [
#             [InlineKeyboardButton("🌐 Register on Website", url="https://www.deimr.com")],
#             [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await update.message.reply_text(
#             "❌ Email not found. Please register on our website to use the bot's services.",
#             reply_markup=reply_markup,
#         )

# # Step 3: Handle OTP Input
# async def handle_otp(update: Update, context: CallbackContext):
#     """Handle OTP input."""
#     if context.user_data.get("state") != "orders:awaiting_otp":
#         return  # Ignore if not in the correct state

#     otp = update.message.text
    # email = context.user_data.get("email")
    # user_data = users_db.get(email)

#     if user_data and otp == user_data["otp"]:
#         # Authenticate the user
#         user_id = update.effective_user.id
#         authenticated_users[user_id] = datetime.now() + timedelta(hours=1)  # 1-hour session
#         await update.message.reply_text("✅ Authentication successful! You can now access your orders for the next 1 hour.")

#         # Clear the awaiting_otp state
#         context.user_data.pop("state", None)

#         await show_orders_menu(update, context)
#     else:
#         await update.message.reply_text("❌ Invalid OTP. Please try again.")



# everything up hre works perfectly updating code for modularity sake and centrlized authentication system

# Start Orders Flow
async def start_orders(update: Update, context: CallbackContext):
    await start_authentication(update, context, "orders")

# Handle Email Input for Orders
async def handle_orders_email(update: Update, context: CallbackContext):
    await handle_email_input(update, context, "orders")

# Handle OTP Input for Orders
async def handle_orders_otp(update: Update, context: CallbackContext):
    email = context.user_data.get("email")
    user_data = users_db.get(email)
    await handle_otp_input(update, context, "orders", await show_orders_menu(update, context))

# Step 4: Show Orders Menu
async def show_orders_menu(update: Update, context: CallbackContext):
    """Display the orders menu."""
    buttons = [
        InlineKeyboardButton(" View Pending Orders", callback_data="view_pending_orders"),
        InlineKeyboardButton(" Track an Order", callback_data="track_order"),
        InlineKeyboardButton(" View Order History", callback_data="view_order_history"),
        InlineKeyboardButton(" Chat with Seller", callback_data="chat_with_seller"),
        InlineKeyboardButton(" Back to Main Menu", callback_data="main_menu"),
    ]
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("Select an option:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Select an option:", reply_markup=reply_markup)

# Step 5: View Pending Orders
async def view_pending_orders(update: Update, context: CallbackContext):
    """Display the user's pending orders."""
    query = update.callback_query
    await query.answer()

    email = context.user_data.get("email")
    pending_orders = users_db.get(email, {}).get("orders", {}).get("pending_orders", [])

    if not pending_orders:
        await query.edit_message_text("You have no pending orders.")
        return

    # Display pending orders
    orders_text = "\n".join(
        [f"{i + 1}️⃣ [Order {order['id']}: {order['product']}, {order['price']}]" for i, order in enumerate(pending_orders)]
    )
    buttons = [InlineKeyboardButton(f"{i + 1}️⃣", callback_data=f"order_details_{order['id']}") for i, order in enumerate(pending_orders)]
    buttons.append(InlineKeyboardButton("🔙 Back to Orders Menu", callback_data="orders_menu"))
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Here are your pending orders:\n{orders_text}", reply_markup=reply_markup)

# Step 6: Track an Order
async def track_order(update: Update, context: CallbackContext):
    """Prompt the user to enter an Order ID."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("Enter your Order ID to track your order:")

    # Set the state to wait for Order ID
    context.user_data["state"] = "orders:awaiting_order_id"

# Step 7: Handle Order ID Input
async def handle_order_id(update: Update, context: CallbackContext):
    """Handle order ID input."""
    if context.user_data.get("state") != "orders:awaiting_order_id":
        return  # Ignore if not in the correct state

    email = context.user_data.get("email")
    order_id = update.message.text

    # Find the order in the database
    orders = users_db.get(email, {}).get("orders", {})
    order = next((o for o in orders.get("pending_orders", []) if o["id"] == order_id), None)

    if not order:
        await update.message.reply_text("❌ Order not found. Please check the Order ID and try again.")
        return

    # Display order details
    order_text = (
        f"🛒 Order Summary:\n"
        f"📦 Order ID: {order['id']}\n"
        f"🛍️ Items: {order['product']}, {order['price']}\n"
        f"🚚 Status: {order['status']}\n\n"
        f"If your order is still pending, you can contact the seller."
    )
    keyboard = [
        [InlineKeyboardButton("1️⃣ Reply with a message to send to the seller", callback_data=f"contact_seller_{order['id']}")],
        [InlineKeyboardButton("2️⃣ Back to Orders Menu", callback_data="orders_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(order_text, reply_markup=reply_markup)

    # Clear the awaiting_order_id state
    context.user_data.pop("state", None)

async def contact_seller(update: Update, context: CallbackContext):
    """Handle the 'Contact Seller' button click."""
    query = update.callback_query
    await query.answer()

    # Extract the order ID from the callback data
    order_id = query.data.split("_")[-1]

    # Store the order ID in context.user_data for future reference
    context.user_data["order_id"] = order_id

    # Prompt the user to enter a message for the seller
    await query.edit_message_text("Please enter your message for the seller:")

    # Set the state to wait for the message
    context.user_data["state"] = "orders:awaiting_seller_message"

# view order history 
async def view_order_history(update: Update, context: CallbackContext):
    """Display the user's order history."""
    query = update.callback_query
    await query.answer()

    # Retrieve the email from context.user_data
    email = context.user_data.get("email")
    if not email:
        await query.edit_message_text("❌ You are not authenticated. Please start the authentication process.")
        return

    # Fetch the user's order history from the database
    order_history = users_db.get(email, {}).get("orders", {}).get("order_history", [])

    if not order_history:
        await query.edit_message_text("You have no order history.")
        return

    # Display order history
    orders_text = "\n".join(
        [f"{i + 1}️⃣ [Order {order['id']}: {order['product']}, {order['price']}, Status: {order['status']}]"
         for i, order in enumerate(order_history)]
    )

    # Add a "Back to Orders Menu" button
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Orders Menu", callback_data="orders_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Here is your order history:\n{orders_text}", reply_markup=reply_markup)

# Step 8: Chat with Seller
async def chat_with_seller(update: Update, context: CallbackContext):
    """Prompt the user to enter a message for the seller."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("Please enter your message for the seller:")

    # Set the state to wait for the message
    context.user_data["state"] = "orders:awaiting_seller_message"

# Step 9: Handle Seller Message
async def handle_seller_message(update: Update, context: CallbackContext):
    """Send the user's message to the seller and await a response."""
    if context.user_data.get("state") != "awaiting_seller_message":
        return  # Ignore if not in the correct state

    message = update.message.text
    email = context.user_data.get("email")
    order_id = context.user_data.get("order_id")

    # Fetch the order details
    order = next((o for o in users_db.get(email, {}).get("orders", {}).get("pending_orders", []) if o["id"] == order_id), None)
    if not order:
        await update.message.reply_text("❌ Order not found. Please try again.")
        return

    # Get the seller ID from the order
    seller_id = order.get("seller_id")
    if not seller_id:
        await update.message.reply_text("❌ Seller not found. Please contact support.")
        return

    # Forward the message to the seller (simulated for now)
    await update.message.reply_text(f"Message sent to seller (ID: {seller_id}): \"{message}\"\nAwaiting seller response...")

    # Store the seller ID and buyer's message in context.user_data
    context.user_data["seller_id"] = seller_id
    context.user_data["buyer_message"] = message

    # Set the state to wait for the seller's response
    context.user_data["state"] = "awaiting_seller_response"

# Step 10: Handle Seller Response
async def handle_seller_response(update: Update, context: CallbackContext):
    """Relay the seller's response to the user."""
    if context.user_data.get("state") != "orders:awaiting_seller_response":
        return  # Ignore if not in the correct state

    seller_response = update.message.text
    buyer_message = context.user_data.get("buyer_message")
    seller_id = context.user_data.get("seller_id")

    # Simulate forwarding the seller's response to the buyer
    await update.message.reply_text(f"📩 Message from seller (ID: {seller_id}):\n\"{seller_response}\"")

    # Clear the state
    context.user_data.pop("state", None)
    context.user_data.pop("seller_id", None)
    context.user_data.pop("buyer_message", None)


# Dispatch messages to the appropriate handler based on the current state
async def handle_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate handler based on the current state."""
    state = context.user_data.get("state")
    print(f"Current state: {state}")  # Debugging: Print the current state
    print(f"Received message: {update.message.text}")  # Debugging: Print the received message

    if state == "orders:awaiting_email":
        # await handle_email(update, context)
        await handle_orders_email(update, context)
    elif state == "orders:awaiting_otp":
        # await handle_otp(update, context)
        await handle_orders_otp(update, context)
    elif state == "orders:awaiting_order_id":
        await handle_order_id(update, context)
    elif state == "orders:awaiting_seller_message":
        await handle_seller_message(update, context)
    elif state == "orders:awaiting_seller_response":
        await handle_seller_response(update, context)
    else:
        # Handle unexpected messages
        await update.message.reply_text("Please start the process by entering your email.")

# Register handlers
orders_handlers = [
    CallbackQueryHandler(start_orders, pattern="^orders$"),
    CallbackQueryHandler(show_orders_menu, pattern="^orders_menu$"),
    CallbackQueryHandler(view_pending_orders, pattern="^view_pending_orders$"),
    CallbackQueryHandler(view_order_history, pattern="^view_order_history$"),
    CallbackQueryHandler(track_order, pattern="^track_order$"),
     CallbackQueryHandler(contact_seller, pattern="^contact_seller_"),
    CallbackQueryHandler(chat_with_seller, pattern="^chat_with_seller$"),
    # MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
]



# Up here works perfectly, updated the file for modularity in implementing authentication


