from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

TOKEN = os.getenv("BOT_TOKEN") or "BOT_TOKEN"
ID_FILE = "ids.json"

if os.path.exists(ID_FILE):
    with open(ID_FILE, "r") as f:
        ids = json.load(f)
else:
    ids = {"bigo": [], "tiktok": []}

def save_ids():
    with open(ID_FILE, "w") as f:
        json.dump(ids, f)

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /add <bigo/tiktok> <ID>")
        return

    platform = context.args[0].lower()
    user_id = context.args[1]

    if platform not in ids:
        await update.message.reply_text("Platform bigo veya tiktok olmalı")
        return

    if user_id not in ids[platform]:
        ids[platform].append(user_id)
        save_ids()

    await update.message.reply_text(
        f"{platform.upper()} ID’leri:\n" + "\n".join(ids[platform])
    )

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /remove <bigo/tiktok> <ID>")
        return

    platform = context.args[0].lower()
    user_id = context.args[1]

    if platform in ids and user_id in ids[platform]:
        ids[platform].remove(user_id)
        save_ids()

    await update.message.reply_text(
        f"Güncel {platform.upper()} ID’leri:\n" + "\n".join(ids[platform])
    )

async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    for plat in ids:
        msg += f"{plat.upper()}:\n"
        msg += "\n".join(ids[plat]) + "\n\n"
    await update.message.reply_text(msg or "Hiç ID yok")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))
app.add_handler(CommandHandler("list", list_ids))

print("🤖 Bot çalışıyor...")
app.run_polling()
