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

# ===== CONFIG =====
TOKEN = "7822123802:AAFYac_ePTxooG5Jm2YlpjiskF7iJnZk7jc"
ADMIN_IDS = [6640151906]
DATA_FILE = "users.json"
ADS = ["https://t.me/helperPhoto1/74"]

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
    "✔️ဒီနေပဲ Jackpot ကျလို့ သူဌေးဖြစ်နိုင်တယ်ရှင့်✔️"
]

# ===== LOGGING =====
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

# ===== USER MANAGEMENT =====
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
        new_user = {"id": chat_id, "username": username, "first_name": first_name}
        users.append(new_user)
        save_users(users)
        return new_user
    return None

async def notify_admins(new_user):
    text = (
        f"🔔 New user joined!\n\n"
        f"👤 Name: {new_user.get('first_name')}\n"
        f"🆔 ID: <code>{new_user.get('id')}</code>\n"
        f"💬 Username: @{new_user.get('username') or 'N/A'}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await app.bot.send_message(admin_id, text, parse_mode="HTML")
        except:
            pass

def add_mau_user(chat_id):
    mau_month = datetime.now().strftime("%Y-%m")
    mau_file = f"data/mau/{mau_month}.json"
    os.makedirs(os.path.dirname(mau_file), exist_ok=True)

    mau_users = []
    if os.path.exists(mau_file):
        with open(mau_file, "r") as f:
            mau_users = json.load(f)

    if chat_id not in mau_users:
        mau_users.append(chat_id)
        with open(mau_file, "w") as f:
            json.dump(mau_users, f)

# ===== HANDLERS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    chat_id = update.effective_chat.id
    new_user = add_user(update)
    add_mau_user(chat_id)

    if new_user:
        await notify_admins(new_user)

    # First two welcome lines
    for msg in WELCOME_MESSAGES[:2]:
        await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(1)
        await context.bot.send_message(chat_id, msg)
        await asyncio.sleep(0.5)

    # Send image
    for url in ADS:
        await context.bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
        await asyncio.sleep(1)
        await context.bot.send_photo(chat_id, photo=url)
        await asyncio.sleep(0.5)

    # Rest of the message
    for msg in WELCOME_MESSAGES[2:]:
        await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(1)
        await context.bot.send_message(chat_id, msg)
        await asyncio.sleep(0.5)

    # Contact buttons
    buttons = [
        [InlineKeyboardButton("① 💎 Agent 1", url="https://t.me/Batman_Unit")],
        [InlineKeyboardButton("② 🔥 Agent 2", url="https://t.me/JulyMoe786")],
        [InlineKeyboardButton("③ 💰 Agent 3", url="https://t.me/WineLay558")],
    ]
    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(1)
    await context.bot.send_message(
        chat_id,
        "📩 ဆက်သွယ်ရန် - အောက်က Button 3 ချက်မှတဆင့် ဆက်သွယ်နိုင်ပါတယ်ရှင့်",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    await update.message.reply_text("📢 ပေးပို့မည့် message ကိုဖြည့်ပါ")
    context.user_data["awaiting_broadcast"] = True

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_broadcast"):
        context.user_data["broadcast_message"] = update.message.text
        await update.message.reply_text(
            f"🔍 Preview:\n\n{update.message.text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirm", callback_data="broadcast_confirm")],
                [InlineKeyboardButton("❌ Cancel", callback_data="broadcast_cancel")],
            ])
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
            except:
                continue
        await query.edit_message_text(f"✅ Sent to {count} users.")
    else:
        await query.edit_message_text("❌ Cancelled.")

async def total_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        users = load_users()
        await update.message.reply_text(f"📊 Total Users: {len(users)}")

async def mau_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    mau_month = datetime.now().strftime("%Y-%m")
    mau_file = f"data/mau/{mau_month}.json"
    if not os.path.exists(mau_file):
        await update.message.reply_text("📊 This month's MAU: 0 users")
        return
    with open(mau_file, "r") as f:
        mau_users = json.load(f)
    await update.message.reply_text(f"📊 MAU: {len(mau_users)} users")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❗ ကျေးဇူးပြုပြီး /start ကိုနှိပ်ပါ။")

# ===== MAIN =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast_command))
app.add_handler(CommandHandler("total", total_users))
app.add_handler(CommandHandler("mau", mau_command))
app.add_handler(CallbackQueryHandler(broadcast_buttons, pattern="^broadcast_"))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_IDS) & ~filters.COMMAND, handle_broadcast))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

def main():
    app.run_polling()

if __name__ == "__main__":
    main()
