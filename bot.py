from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes
import uuid

import api_connect
import config

def add_user(duration_days, data_gb, username):
    try:
        duration_days = int(duration_days)
        data_gb = int(data_gb)
        username = str(username)
        result = api_connect.ahriman_add_user(duration_days, data_gb, username)
        url = config.ahriman_url
        return url + result['subscription_url']
    except Exception as e:
        return None

def generate_message(subscription_link):
    message = (
        "✅ Your VPN account has been successfully created!\n\n"
        "Subscription Link:\n"
        f"{subscription_link}\n\n"
        "To use the VPN:\n"
        "1. Open the link in your browser or import it in the V2Ray client.\n"
        "2. Choose your preferred connection type and connect.\n\n"
        "If you have any questions or issues, feel free to contact TechnicalNet support.\n"
        "Best regards,\n"
        "TechnicalNet Team"
    )
    return message

TOKEN = config.ahriman_token
ADMINS = config.ahriman_admin
TEST_DURATION = config.ahriman_test_time
TEST_DATA = config.ahriman_test_data

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.inline_query.from_user.id
    query = update.inline_query.query.strip().lower()

    def is_admin(user_id):
        return user_id in ADMINS

    if not is_admin(user_id):
        await update.inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Access Denied",
                    input_message_content=InputTextMessageContent("You are not authorized to use this bot.")
                )
            ],
            cache_time=0
        )
        return

    results = []

    if query.startswith("user"):
        parts = query.split()
        if len(parts) != 4:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Invalid Input Format",
                    input_message_content=InputTextMessageContent("Correct format: user <days> <username> <data_GB>"),
                    description="Example: user 30 john 10"
                )
            )
        else:
            _, days, username, data = parts
            link = add_user(days, data, username)
            if link:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title=f"{username} - {data} GB",
                        input_message_content=InputTextMessageContent(generate_message(link)),
                        description="Account created successfully"
                    )
                )
            else:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="Error",
                        input_message_content=InputTextMessageContent("An error occurred while creating the account."),
                        description="Check the input values."
                    )
                )

    elif query.startswith("test"):
        parts = query.split()
        if len(parts) != 2:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Invalid Input Format",
                    input_message_content=InputTextMessageContent("Correct format: test <username>"),
                    description="Example: test john"
                )
            )
        else:
            _, username = parts
            link = add_user(TEST_DURATION, TEST_DATA, username)
            if link:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title=f"Test Account for {username}",
                        input_message_content=InputTextMessageContent(generate_message(link)),
                        description="Test account created"
                    )
                )
            else:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="Error",
                        input_message_content=InputTextMessageContent("An error occurred while creating the test account."),
                        description="Please try again later."
                    )
                )

    if results:
        await update.inline_query.answer(results, cache_time=1)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query_handler))

print("Bot is running...")
app.run_polling()
