from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime
from app.utils.database import messages_db
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Helper function to chunk buttons into rows of 2
def chunk_buttons(buttons, row_size=2):
    return [buttons[i:i + row_size] for i in range(0, len(buttons), row_size)]

# Step 1: Start Messages Flow
async def start_messages(update: Update, context: CallbackContext):
    """Display a list of buyers with their last message."""
    # Set the state to "messages:viewing_buyers"
    context.user_data["state"] = "messages:viewing_buyers"

    # Create buttons for each buyer
    buttons = []
    for buyer, messages in messages_db.items():
        last_message = messages[-1]["message"]
        timestamp = messages[-1]["timestamp"]
        button_text = f"{buyer}: {last_message} ({timestamp})"
        buttons.append(InlineKeyboardButton(button_text, callback_data=f"view_chat:{buyer}"))

    # Add a "Back to Seller Menu" button
    buttons.append(InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu"))

    # Chunk buttons into rows of 2
    keyboard = chunk_buttons(buttons, row_size=2)
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("📩 Buyer Messages:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("📩 Buyer Messages:", reply_markup=reply_markup)

# Step 2: View Chat with a Buyer
async def view_chat(update: Update, context: CallbackContext):
    """Display the chat history with a specific buyer."""
    query = update.callback_query
    await query.answer()

    # Extract the buyer's email from the callback data
    buyer_email = query.data.split(":")[1]
    context.user_data["current_buyer"] = buyer_email

    # Set the state to "messages:viewing_chat"
    context.user_data["state"] = "messages:viewing_chat"

    # Fetch the chat history
    chat_history = messages_db.get(buyer_email, [])
    chat_text = "\n".join(
        [f"{msg['sender']} ({msg['timestamp']}): {msg['message']}" for msg in chat_history]
    )

    # Create buttons for navigation
    keyboard = [
        [InlineKeyboardButton("✍ Respond", callback_data=f"respond:{buyer_email}")],
        [InlineKeyboardButton("🔙 Back to Messages", callback_data="messages")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"💬 Chat with {buyer_email}:\n\n{chat_text}", reply_markup=reply_markup)

# Step 3: Respond to a Buyer
async def respond_to_buyer(update: Update, context: CallbackContext):
    """Prompt the seller to type a response while retaining the chat history."""
    query = update.callback_query
    await query.answer()

    # Set the state to "messages:awaiting_response"
    context.user_data["state"] = "messages:awaiting_response"

    # Fetch the chat history
    buyer_email = context.user_data.get("current_buyer")
    chat_history = messages_db.get(buyer_email, [])
    chat_text = "\n".join(
        [f"{msg['sender']} ({msg['timestamp']}): {msg['message']}" for msg in chat_history]
    )

    # Create buttons for navigation
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Messages", callback_data="messages")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Display the chat history with the prompt to type a response
    await query.edit_message_text(
        f"💬 Chat with {buyer_email}:\n\n{chat_text}\n\nType your response:",
        reply_markup=reply_markup,
    )

# Step 4: Handle Seller's Response
async def handle_seller_response(update: Update, context: CallbackContext):
    """Send the seller's response to the buyer and update the chat history."""
    if context.user_data.get("state") != "messages:awaiting_response":
        return  # Ignore if not in the correct state

    seller_response = update.message.text
    buyer_email = context.user_data.get("current_buyer")

    # Add the seller's response to the chat history
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages_db[buyer_email].append({
        "sender": "seller@example.com",
        "message": seller_response,
        "timestamp": timestamp,
    })

    # Notify the seller
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Messages", callback_data="messages")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "✅ Message sent. Awaiting buyer response...",
        reply_markup=reply_markup,
    )

    # Clear the state
    context.user_data.pop("state", None)
    context.user_data.pop("current_buyer", None)

# Step 5: Dispatch Messages to the Appropriate Handler
async def handle_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate handler based on the current state."""
    state = context.user_data.get("state")
    logger.info(f"Current state: {state}")
    logger.info(f"Received message: {update.message.text}")

    if state == "messages:awaiting_response":
        await handle_seller_response(update, context)
    else:
        await update.message.reply_text("Please select an option from the menu.")

# Register handlers
messages_handlers = [
    CallbackQueryHandler(start_messages, pattern="^messages$"),
    CallbackQueryHandler(view_chat, pattern="^view_chat:"),
    CallbackQueryHandler(respond_to_buyer, pattern="^respond:"),
    CallbackQueryHandler(start_messages, pattern="^messages$"),  # Back to Messages
]