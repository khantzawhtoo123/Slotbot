import json
import os
import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ========== CONFIG ==========
TOKEN = "7822123802:AAFYac_ePTxooG5Jm2YlpjiskF7iJnZk7jc"
ADMIN_IDS = [6640151906]
DATA_FILE = "users.json"

ADS = [
    "https://t.me/helperPhoto1/74",
]

WELCOME_MESSAGES = [
    "မင်္ဂလာပါ 🩷",
    "Batman688 စလော့ဂိမ်းအေးဂျင့် မှကြိုဆိုပါတယ် 🥰",
    "♾မြန်မာနိုင်ငံရဲ့နံပါတ်⚡️Game ဆိုဒ်ကြီးမှာ♾\n\n"
    "➡️မစမ်းကြည့်သေးဘူးဆိုရင် မင်း\n\n"
    "💯 ငွေဖြင့် Legendary ဖြစ်နိုင်တဲ့\n"
    "💯အခွင့်အလမ်းလက်လွှတ်နေပြီ!\n\n"
    "💯အလျော်အစားမှန်ကန်ပြီး ငွေကြေးအာမခံမှုရှိတဲ့အေးဂျင့် \n\n"
    "😞PP အွန်လိုင်းဂိမ်းတစ်ခုကနေ သင်အနေနဲ့ \n\n"
    "📌 3000 ကျပ်ရှိရုံနဲ့စတင်လို့ရပါပြီ\n"
    "📌Bonus အပြည့်, Cashback ရရှိမယ်, \n\n"
    "✔️ နာမည်ကြီး Game များဖြစ်တဲ့\n"
    "✔️Gates of Olympus \n"
    "✔️Sugar Rush\n"
    "✔️Starlight Princess\n"
    "✔️Sweet Bonanza\n"
    "✔️Pyramid Bonanza\n\n"
    "✔️အမိုက်စား Promotion တွေ\n"
    "✔️မန်ဘာသစ် Double Bonus\n"
    "✔️ရှုံးကြေး 30% Cashback\n"
    "✔️နေ့စဉ်ငွေသွင်း 50% Bonus\n"
    "✔️နိုင်ကြေးပြန်အမ်း 100%\n"
    "✔️ပိတ်ခန်းမရှိဘူး! ပျော်ချင်လားငွေနဲ့စွန့်စားချင်လား\n\n"
    "✔️တစ်ချက်တင်ပြီး Game Master ဖြစ်ရအောင်!\n"
    "✔️သူများတွေအနိုင်ရတာကြည့်နေမလား။\n"
    "✔️မင်းလည်းဝင်ကစားလိုက်တော့!\n"
    "✔️ဒီနေပဲ Jackpot ကျလို့ သူဌေးဖြစ်နိုင်တယ်ရှင့်✔️",
]

# ========== LOGGING ==========
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ========== UTILS ==========
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

def add_user(update: Update):
    users = load_users()
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name

    if not any(u["id"] == chat_id for u in users):
        users.append({"id": chat_id, "username": username, "first_name": first_name})
        save_users(users)
        print(f"✅ New user stored: {chat_id} - {username}")

def add_mau_user(chat_id):
    mau_month = datetime.now().strftime("%Y-%m")
    mau_file = f"data/mau/{mau_month}.json"
    os.makedirs(os.path.dirname(mau_file), exist_ok=True)

    if os.path.exists(mau_file):
        with open(mau_file, "r") as f:
            mau_users = json.load(f)
    else:
        mau_users = []

    if chat_id not in mau_users:
        mau_users.append(chat_id)
        with open(mau_file, "w") as f:
            json.dump(mau_users, f)
        print(f"📈 MAU updated for {chat_id}")

# ========== HANDLERS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    add_user(update)
    add_mau_user(chat_id)

    # Show typing action
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    await asyncio.sleep(1)

    # Send welcome messages
    for msg in WELCOME_MESSAGES:
        await context.bot.send_message(chat_id=chat_id, text=msg)
        await asyncio.sleep(0.5)

    # Send image in the middle
    for url in ADS:
        await context.bot.send_photo(chat_id=chat_id, photo=url)
        await asyncio.sleep(0.5)

    # Send contact buttons
    buttons = [
        [InlineKeyboardButton("Agent ❤️", url="https://t.me/Batman_Unit")],
        [InlineKeyboardButton("Agent ❤️", url="https://t.me/JulyMoe786")],
        [InlineKeyboardButton("Agent ❤️", url="https://t.me/WineLay558")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(
        chat_id=chat_id,
        text="📩 ဆက်သွယ်ရန် - အောက်က Button 3 ချက်မှတဆင့် ဆက်သွယ်နိုင်ပါတယ်ရှင့်",
        reply_markup=reply_markup,
    )

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ You are not authorized.")
        return
    await update.message.reply_text("📢 Broadcast ပို့မည့် message ကိုပေးပို့ပါ။")
    context.user_data["awaiting_broadcast"] = True

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_broadcast"):
        context.user_data["broadcast_message"] = update.message.text
        await update.message.reply_text(
            f"🔍 Preview:\n\n{update.message.text}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("✅ Confirm", callback_data="broadcast_confirm")],
                    [InlineKeyboardButton("❌ Cancel", callback_data="broadcast_cancel")],
                ]
            ),
        )
        context.user_data["awaiting_broadcast"] = False

async def broadcast_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    users = load_users()

    if query.data == "broadcast_confirm":
        msg = context.user_data.get("broadcast_message", "")
        count = 0
        for user in users:
            try:
                await context.bot.send_message(chat_id=user["id"], text=msg)
                count += 1
            except Exception as e:
                print(f"❌ Error sending to {user['id']}: {e}")
        await query.edit_message_text(f"✅ Broadcast sent to {count} users.")
    else:
        await query.edit_message_text("❌ Broadcast cancelled.")

async def total_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ You are not authorized.")
        return
    users = load_users()
    await update.message.reply_text(f"📊 Total Users: {len(users)}")

async def mau_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("⛔ You are not authorized.")
        return

    mau_month = datetime.now().strftime("%Y-%m")
    mau_file = f"data/mau/{mau_month}.json"

    if not os.path.exists(mau_file):
        await update.message.reply_text("📊 This month's MAU: 0 users")
        return

    with open(mau_file, "r") as f:
        mau_users = json.load(f)

    await update.message.reply_text(f"📊 MAU for {mau_month}: {len(mau_users)} users")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❗ ကျေးဇူးပြုပြီး /start ကိုနှိပ်ပါ။ Bot သုံးရန် အစပြုနိုင်ပါတယ်။")

# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("total", total_users))
    app.add_handler(CommandHandler("mau", mau_command))
    app.add_handler(CallbackQueryHandler(broadcast_buttons, pattern="^broadcast_"))

    app.add_handler(MessageHandler(
        filters.TEXT & filters.User(user_id=ADMIN_IDS) & ~filters.COMMAND,
        handle_broadcast
    ))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    app.run_polling()

if __name__ == "__main__":
    main()