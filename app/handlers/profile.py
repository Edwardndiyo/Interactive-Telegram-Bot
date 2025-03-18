from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime, timedelta
from utils.database import users_db

from services.authentication import start_authentication, handle_email_input, handle_otp_input


# authenticated_users = {}

# # Step 1: Start Profile Flow
# async def start_profile(update: Update, context: CallbackContext):
#     """Prompt user to enter their email."""
#     if update.callback_query:
#         query = update.callback_query
#         await query.answer()
#         message = query.message
#     else:
#         message = update.message

#     await message.reply_text("Please enter your registered email address:")

#     # Set the state to wait for email
#     context.user_data["state"] = "profile:awaiting_email"

# # Step 2: Handle Email Input
# async def handle_email(update: Update, context: CallbackContext):
#     """Handle email input."""
#     if context.user_data.get("state") != "profile:awaiting_email":
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
#         context.user_data["state"] = "profile:awaiting_otp"
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
#     """Handle OTP input for profile access."""
#     if context.user_data.get("state") != "profile:awaiting_otp":
#         return  # Ignore if not in the correct state

#     otp = update.message.text
#     email = context.user_data.get("email")
#     user_data = users_db.get(email)

#     # Check if OTP is correct
#     if user_data and otp == user_data["otp"]:
#         # Authenticate the user
#         user_id = update.effective_user.id
#         authenticated_users[user_id] = datetime.now() + timedelta(hours=1)  # 1-hour session

#         # Clear the awaiting_otp state
#         context.user_data.pop("state", None)

#         # Display profile details
#         await display_profile(update, context, user_data)
#     else:
#         await update.message.reply_text("❌ Invalid OTP. Please try again.")

# up here works perfectly, updating the codebase for sake of modularity

# Start Profile Flow
async def start_profile(update: Update, context: CallbackContext):
    await start_authentication(update, context, "profile")

# Handle Email Input for Profile
async def handle_profile_email(update: Update, context: CallbackContext):
    await handle_email_input(update, context, "profile")

async def handle_profile_otp(update: Update, context: CallbackContext):
    await handle_otp_input(update, context, "profile", display_profile)

# Step 4: Display Profile Details
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

# Step 5: Dispatch Messages
async def handle_profile_message(update: Update, context: CallbackContext):
    """Dispatch messages to the appropriate handler based on the current state."""
    state = context.user_data.get("state")
    print(f"Current state: {state}")  # Debugging: Print the current state
    print(f"Received message: {update.message.text}")  # Debugging: Print the received message

    if state == "profile:awaiting_email":
        # await handle_email(update, context)
        await handle_profile_email(update, context)
    elif state == "profile:awaiting_otp":
        # await handle_otp(update, context)
        await handle_profile_otp(update, context)
    else:
        # Handle unexpected messages
        await update.message.reply_text("Please start the process by selecting the 'Profile' option.")

# Register handlers
profile_handlers = [
    CallbackQueryHandler(start_profile, pattern="^profile$"),
    # MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_message),
]