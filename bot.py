from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes
import uuid

import api_connect
import config

def adduser(tb_time, tb_data, tb_name):
    try:
        tb_time = int(tb_time)
        tb_data = int(tb_data)
        tb_name = str(tb_name)
        result = api_connect.ahriman_add_user(tb_time, tb_data, tb_name)
        url = config.ahriman_url
        return url + result['subscription_url']
    except Exception as e:
        return None

def msg(link):
    msg_vpn = (
        "✅ اکانت شما با موفقیت ساخته شد!\n\n"
        "لینک اشتراک شما:\n"
        f"{link}\n\n"
        "برای استفاده:\n"
        "1. لینک بالا را در مرورگر باز کرده یا در برنامه V2RAY وارد کنید.\n"
        "2. نوع اتصال مورد نظر را انتخاب کرده و متصل شوید.\n\n"
        "در صورت وجود هرگونه سوال یا مشکل، با پشتیبانی تکنیکال نت در تماس باشید.\n"
        "با احترام - تیم تکنیکال نت"
    )
    return msg_vpn

TOKEN = config.ahriman_token
ADMINS = config.ahriman_admin
test_time = config.ahriman_test_time
test_data = config.ahriman_test_data

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
                    title="you aren`t admin",
                    input_message_content=InputTextMessageContent("you aren`t use this bot")
                )
            ],
            cache_time=0
        )
        return

    results = []

    if query.startswith("user"):
        parts = query.split()
        if len(parts) != 5:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="input is wrong",
                    input_message_content=InputTextMessageContent("time name data"),
                    description="example : user 30 name 10"
                )
            )
        else:
            time, name, data = parts[2], parts[3], parts[4]
            link = adduser(time, data, name)
            if link:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title=f"{name} - {data}GB",
                        input_message_content=InputTextMessageContent(msg(link)),
                        description="okay"
                    )
                )
            else:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="error",
                        input_message_content=InputTextMessageContent("error"),
                        description="check input"
                    )
                )

    elif query.startswith("test"):
        parts = query.split()
        if len(parts) != 3:
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="input is wrong",
                    input_message_content=InputTextMessageContent("name"),
                    description="example : test name"
                )
            )
        else:
            name = parts[2]
            link = adduser(test_time, test_data, name)
            if link:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title=f"test for {name}",
                        input_message_content=InputTextMessageContent(msg(link)),
                        description="okay"
                    )
                )
            else:
                results.append(
                    InlineQueryResultArticle(
                        id=str(uuid.uuid4()),
                        title="error",
                        input_message_content=InputTextMessageContent("error"),
                        description="error"
                    )
                )

    if results:
        await update.inline_query.answer(results, cache_time=1)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(InlineQueryHandler(inline_query_handler))

print("bot is runned.")
app.run_polling()