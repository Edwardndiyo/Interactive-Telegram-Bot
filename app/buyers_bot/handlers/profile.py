from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from app.services.authentication import start_authentication, handle_otp_input, handle_email_input

# Start Profile Flow
async def start_profile(update: Update, context: CallbackContext):
    """Start the profile authentication flow."""
    await start_authentication(update, context, "profile")

# Handle Email input for profile
async def handle_profile_email(update:Update, context: CallbackContext):
    """Handle email input for the profile module."""
    await handle_email_input(update, context, "profile")

# Handle OTP Input for Profile
async def handle_profile_otp(update: Update, context: CallbackContext):
    """Handle OTP input for the profile module."""
    await handle_otp_input(update, context, "profile", display_profile)

# Display Profile Details
async def display_profile(update: Update, context: CallbackContext, user_data):
    """Display the user's profile details."""
    name = user_data["name"]
    email = user_data["email"]
    date_joined = user_data.get("date_joined", "Unknown")
    reward_points = user_data.get("reward_points", 0)

    # Format the profile details
    profile_text = (
        "✅ Authentication successful!\n\n\n"
        f"  {name}, Here's your profile information.\n\n"
        f"👤 Name: {name}\n"
        f"📧 Email: {email}\n"
        f"📅 Joined: {date_joined}\n"
        f"💰 Reward Points: {reward_points}\n\n"
    )

    # Create a "Back to Main Menu" button
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(profile_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(profile_text, reply_markup=reply_markup)

# Dispatch Messages
async def handle_profile_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate handler based on the current state."""
    state = context.user_data.get("state")
    print(f"Current state: {state}")  # Debugging: Print the current state
    print(f"Received message: {update.message.text}")  # Debugging: Print the received message

    if state == "profile:awaiting_email":
        await handle_profile_email(update, context)
    elif state == "profile:awaiting_otp":
        await handle_profile_otp(update, context)
    else:
        # Handle unexpected messages
        await update.message.reply_text("Please start the process by selecting the 'Profile' option.")

# Register handlers
profile_handlers = [
    CallbackQueryHandler(start_profile, pattern="^profile$"),
]