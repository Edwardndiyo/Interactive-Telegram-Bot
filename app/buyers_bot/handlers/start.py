from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

async def start(update: Update, context: CallbackContext):
    """Display main menu with options and clear any existing state."""
    # Clear the state when returning to the main menu
    context.user_data.pop("state", None)

    keyboard = [
        [InlineKeyboardButton("Search Product 🔍", callback_data="search_product"), 
         InlineKeyboardButton("Explore 🐛", callback_data="explore_product")],
        [InlineKeyboardButton("User Profile 👤", callback_data="profile"), 
         InlineKeyboardButton("Orders 📦", callback_data="orders")],
        [InlineKeyboardButton("AI Assistant 🤖", callback_data="ai_assistant"),
         InlineKeyboardButton("Quick Comparison ⚖️", callback_data="compare_product")]         
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check if the update is from a CallbackQuery or a direct message
    if update.callback_query:
        # If triggered by a CallbackQuery (e.g., "Back to Main Menu" button)
        query = update.callback_query
        await query.answer()  # Acknowledge the callback
        await query.edit_message_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)
    else:
        # If triggered by a direct message (e.g., /start command)
        await update.message.reply_text("Welcome to Deimr Stella! Please select an option:", reply_markup=reply_markup)

# Register handlers
start_handler = CommandHandler("start", start)
main_menu_handler = CallbackQueryHandler(start, pattern="^main_menu$")



# up here works perfectly implementing grabbing users number for verification - 







# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import CallbackContext, CommandHandler

# from app.utils.database import users_db  # Your mock database

# async def start(update: Update, context: CallbackContext):
#     """Prompt the user to share their phone number."""
#     keyboard = [[KeyboardButton("📱 Share Phone Number", request_contact=True)]]
#     reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

#     await update.message.reply_text("Please share your phone number to proceed.", reply_markup=reply_markup)

#     # Store state in context
#     context.user_data["state"] = "awaiting_phone"

# async def handle_phone_input(update: Update, context: CallbackContext):
#     """Process the shared phone number and fetch user details from the mock database."""
#     if context.user_data.get("state") != "awaiting_phone":
#         return  # Ignore input if not expecting a phone number

#     # Retrieve phone number (either from shared contact or manually entered)
#     phone_number = None
#     if update.message.contact:
#         phone_number = update.message.contact.phone_number
#     elif update.message.text:
#         phone_number = update.message.text  # If user types manually

#     if not phone_number:
#         await update.message.reply_text("Invalid input. Please share a valid phone number.")
#         return

#     # Search for the user in the database
#     user_data = next((data for email, data in users_db.items() if data.get("phone_number") == phone_number), None)

#     if user_data:
#         context.user_data["email"] = user_data["email"]
#         context.user_data["name"] = user_data["name"]
#         welcome_message = f"Welcome back, {user_data['name']}! Please select an option:"
#     else:
#         welcome_message = "Welcome to Deimr Stella! Please register to continue."

#     # Display the main menu
#     keyboard = [
#         [KeyboardButton("Search Product 🔍"), KeyboardButton("Explore 🐛")],
#         [KeyboardButton("User Profile 👤"), KeyboardButton("Orders 📦")],
#         [KeyboardButton("AI Assistant 🤖"), KeyboardButton("Quick Comparison ⚖️")]
#     ]
#     reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

#     await update.message.reply_text(welcome_message, reply_markup=reply_markup)

#     # Reset state
#     context.user_data["state"] = None

# # Register handlers
# start_handlers = [
#     CommandHandler("start", start),
#     # MessageHandler(filters.CONTACT | filters.TEXT, handle_phone_input),  # Ensure this triggers properly
# ]
