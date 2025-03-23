from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime, timedelta
from app.utils.database import users_db
from app.services.authentication import start_authentication, handle_otp_input
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function to chunk buttons into rows of 2
def chunk_buttons(buttons, row_size=2):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

# Start Orders Flow
async def start_orders(update: Update, context: CallbackContext):
    """Start the orders authentication flow."""
    await start_authentication(update, context, "orders")
    logger.info("Orders flow started. State set to 'orders:awaiting_otp'.")

# Handle OTP Input for Orders
async def handle_orders_otp(update: Update, context: CallbackContext):
    """Handle OTP input for the orders module."""
    await handle_otp_input(update, context, "orders", show_orders_menu)

# Step 4: Show Orders Menu
async def show_orders_menu(update: Update, context: CallbackContext):
    """Display the orders menu."""
    buttons = [
        InlineKeyboardButton(" View Pending Orders", callback_data="view_pending_orders"),
        InlineKeyboardButton(" Track an Order", callback_data="track_order"),
        InlineKeyboardButton(" View Order History", callback_data="view_order_history"),
        InlineKeyboardButton(" Chat with Buyer", callback_data="chat_with_buyer"),
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
    logger.info("State set to 'orders:awaiting_order_id'.")

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
        [InlineKeyboardButton("1️⃣ Reply with a message to send to the Buyer", callback_data=f"contact_buyer_{order['id']}")],
        [InlineKeyboardButton("2️⃣ Back to Orders Menu", callback_data="orders_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(order_text, reply_markup=reply_markup)

    # Clear the awaiting_order_id state
    context.user_data.pop("state", None)
    logger.info("State 'orders:awaiting_order_id' cleared.")

# Step 8: Chat with Buyer
async def chat_with_buyer(update: Update, context: CallbackContext):
    """Prompt the user to enter a message for the buyer."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("Please enter your message for the buyer:")

    # Set the state to wait for the message
    context.user_data["state"] = "orders:awaiting_buyer_message"
    logger.info("State set to 'orders:awaiting_buyer_message'.")

# Step 9: Handle Buyer Message
async def handle_buyer_message(update: Update, context: CallbackContext):
    """Send the user's message to the buyer and await a response."""
    if context.user_data.get("state") != "orders:awaiting_buyer_message":
        return  # Ignore if not in the correct state

    message = update.message.text
    email = context.user_data.get("email")
    order_id = context.user_data.get("order_id")

    # Fetch the order details
    order = next((o for o in users_db.get(email, {}).get("orders", {}).get("pending_orders", []) if o["id"] == order_id), None)
    if not order:
        await update.message.reply_text("❌ Order not found. Please try again.")
        return

    # Get the buyer ID from the order
    buyer_id = order.get("buyer_id")
    if not buyer_id:
        await update.message.reply_text("❌ Buyer not found. Please contact support.")
        return

    # Forward the message to the buyer (simulated for now)
    await update.message.reply_text(f"Message sent to buyer (ID: {buyer_id}): \"{message}\"\nAwaiting buyer response...")

    # Store the buyer ID and message in context.user_data
    context.user_data["buyer_id"] = buyer_id
    context.user_data["buyer_message"] = message

    # Set the state to wait for the buyer's response
    context.user_data["state"] = "orders:awaiting_buyer_response"
    logger.info("State set to 'orders:awaiting_buyer_response'.")

# Step 10: Handle Buyer Response
async def handle_buyer_response(update: Update, context: CallbackContext):
    """Relay the buyer's response to the user."""
    if context.user_data.get("state") != "orders:awaiting_buyer_response":
        return  # Ignore if not in the correct state

    buyer_response = update.message.text
    buyer_message = context.user_data.get("buyer_message")
    buyer_id = context.user_data.get("buyer_id")

    # Simulate forwarding the buyer's response to the user
    await update.message.reply_text(f"📩 Message from buyer (ID: {buyer_id}):\n\"{buyer_response}\"")

    # Clear the state
    context.user_data.pop("state", None)
    context.user_data.pop("buyer_id", None)
    context.user_data.pop("buyer_message", None)
    logger.info("State 'orders:awaiting_buyer_response' cleared.")

# Dispatch messages to the appropriate handler based on the current state
async def handle_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate handler based on the current state."""
    state = context.user_data.get("state")
    logger.info(f"Current state: {state}")
    logger.info(f"Received message: {update.message.text}")

    # if state == "orders:awaiting_email":
    #     await handle_orders_email(update, context)
    if state == "orders:awaiting_otp":
        await handle_orders_otp(update, context)
    elif state == "orders:awaiting_order_id":
        await handle_order_id(update, context)
    elif state == "orders:awaiting_buyer_message":
        await handle_buyer_message(update, context)
    elif state == "orders:awaiting_buyer_response":
        await handle_buyer_response(update, context)
    else:
        # Handle unexpected messages
        await update.message.reply_text("Please start the process by entering your email.")

# Register handlers
orders_handlers = [
    CallbackQueryHandler(start_orders, pattern="^orders$"),
    CallbackQueryHandler(show_orders_menu, pattern="^orders_menu$"),
    CallbackQueryHandler(view_pending_orders, pattern="^view_pending_orders$"),
    CallbackQueryHandler(track_order, pattern="^track_order$"),
    CallbackQueryHandler(chat_with_buyer, pattern="^chat_with_buyer$"),
]