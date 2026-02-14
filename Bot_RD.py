import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading

TOKEN = "8132249695:AAGXBuNoqXTDCsuyGCzVCANtS5SWRy2hWsI"
CHANNEL_ID = -1002696090717   # آیدی کانال
ADMIN_ID = 7796569566
DELETE_DELAY = 20  # ثانیه

bot = telebot.TeleBot(TOKEN)

# ---------- حذف خودکار ----------
def delete_message_safe(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

def send_user_message(chat_id, text, reply_markup=None):
    msg = bot.send_message(chat_id, text, reply_markup=reply_markup)
    threading.Timer(
        DELETE_DELAY,
        lambda: delete_message_safe(chat_id, msg.message_id)
    ).start()

# ---------- /start ----------
@bot.message_handler(commands=['start'])
def start_message(message):

    user_id = message.from_user.id
    user_name = message.from_user.username or message.from_user.first_name

    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        status = member.status
    except:
        status = "left"

    # ---------- عضو بود ----------
    if status in ["member", "administrator", "creator"]:

        send_user_message(
            user_id,
            "✅ شما عضو کانال هستید"
        )

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "🚫 بن کردن کاربر از کانال",
                callback_data=f"ban_{user_id}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            f"✅ کاربر استارت زد و عضو کانال است\n\n"
            f"👤 نام: {user_name}\n"
            f"🆔 آیدی: {user_id}",
            reply_markup=keyboard
        )

    # ---------- عضو نبود ----------
    else:

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "📢 عضویت در کانال",
                url="https://t.me/+-WPMFiNRJMZmZTRk"
            )
        )

        send_user_message(
            user_id,
            "برای عضویت در چنل رو دکمه زیر کلیک کنید🤖",
            reply_markup=keyboard
        )

# ---------- هندلر لف ----------
@bot.chat_member_handler()
def handle_left_member(update):

    if update.chat.id != CHANNEL_ID:
        return

    user = update.new_chat_member.user
    user_id = user.id
    user_name = user.username or user.first_name

    old_status = update.old_chat_member.status
    new_status = update.new_chat_member.status

    # اگر لف داد
    if old_status in ["member", "administrator", "creator"] and new_status == "left":

        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(
                "🚫 بن کردن کاربر از کانال",
                callback_data=f"ban_{user_id}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            f"⚠️ کاربر از کانال لف داد\n\n"
            f"👤 نام: {user_name}\n"
            f"🆔 آیدی: {user_id}",
            reply_markup=keyboard
        )

# ---------- بن ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("ban_"))
def ban_user(call):

    user_id = int(call.data.split("_")[1])

    try:
        bot.ban_chat_member(CHANNEL_ID, user_id)

        bot.answer_callback_query(
            call.id,
            "✅ کاربر بن شد"
        )

        bot.send_message(
            call.message.chat.id,
            f"🚫 کاربر {user_id} بن شد."
        )

    except Exception as e:

        bot.answer_callback_query(
            call.id,
            "❌ خطا در بن"
        )

        bot.send_message(
            call.message.chat.id,
            f"خطا:\n{e}"
        )

print("Bot Running ...")

bot.infinity_polling(
    skip_pending=True,
    allowed_updates=[
        "message",
        "callback_query",
        "chat_member"
    ]
)
