# users = {}

# def is_authenticated(user_id):
#     return users.get(user_id, {}).get("authenticated", False)

# def authenticate_user(user_id):
#     users[user_id] = {"authenticated": True}



# up here works perfectly, modularity fix 



from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.database import users_db

# Dictionary to store authenticated users and their session expiry time
authenticated_users = {}


# Function to check if a user is authenticated
def is_authenticated(user_id):
    return user_id in authenticated_users and datetime.now() < authenticated_users[user_id]

# Function to authenticate user
def authenticate_user(user_id):
    authenticated_users[user_id] = datetime.now() + timedelta(hours=1)  # Set session for 1 hour

# Function to start authentication (Email input)
async def start_authentication(update, context, module_name):
    """Prompts the user to enter their email for authentication."""
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        message = query.message
    else:
        message = update.message

    await message.reply_text("Please enter your registered email address:")
    context.user_data["state"] = f"{module_name}:awaiting_email"

# Function to handle email input
async def handle_email_input(update, context, module_name):
    """Handles email verification and sends OTP."""
    expected_state = f"{module_name}:awaiting_email"
    if context.user_data.get("state") != expected_state:
        return  # Ignore if not in the correct state

    email = update.message.text.strip().lower()
    user_data = users_db.get(email)

    if user_data:
        # Store user details and send OTP
        context.user_data["email"] = email
        context.user_data["name"] = user_data["name"]
        await update.message.reply_text(f"Welcome {user_data['name']}, we have sent an OTP to your email. Please provide it here.")
        context.user_data["state"] = f"{module_name}:awaiting_otp"
    else:
        keyboard = [[InlineKeyboardButton("🌐 Register on Website", url="https://www.deimr.com")],
                    [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("❌ Email not found. Please register on our website.", reply_markup=reply_markup)

# Function to handle OTP input
async def handle_otp_input(update, context, module_name, success_callback):
    """Handles OTP verification."""
    expected_state = f"{module_name}:awaiting_otp"
    if context.user_data.get("state") != expected_state:
        return  # Ignore if not in the correct state

    otp = update.message.text
    email = context.user_data.get("email")
    user_data = users_db.get(email)

    if user_data and otp == user_data["otp"]:
        user_id = update.effective_user.id
        authenticate_user(user_id)  # Authenticate user
        context.user_data.pop("state", None)  # Clear state
        # await update.message.reply_text("✅ Authentication successful!")
        
        # Call the module-specific success callback
        await success_callback(update, context, user_data)
    else:
        await update.message.reply_text("❌ Invalid OTP. Please try again.")
