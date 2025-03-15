# from telegram import Update
# from telegram.ext import CallbackContext

# users = {}

# async def check_authentication(update: Update, context: CallbackContext, section: str):
#     """ Check if user is authenticated; if not, ask for email """
#     user_id = update.callback_query.message.chat_id
#     if users.get(user_id, {}).get("authenticated"):
#         await update.callback_query.message.reply_text(f"✅ You are authenticated! Accessing {section}...")
#     else:
#         users[user_id] = {"authenticated": True}
#         await update.callback_query.message.reply_text("Please enter your email to continue.")
# #


users = {}

def is_authenticated(user_id):
    return users.get(user_id, {}).get("authenticated", False)

def authenticate_user(user_id):
    users[user_id] = {"authenticated": True}
