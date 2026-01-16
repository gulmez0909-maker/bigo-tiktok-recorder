# ---------------- bot.py v20+ ----------------
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os

TOKEN = "BOT_TOKEN"  # GitHub Secrets veya lokal test için token
ID_FILE = "ids.json"

# IDs dosyasını yükle veya oluştur
if os.path.exists(ID_FILE):
    with open(ID_FILE, "r") as f:
        ids = json.load(f)
else:
    ids = {"bigo": [], "tiktok": []}

def save_ids():
    with open(ID_FILE, "w") as f:
        json.dump(ids, f)

# ----- Komutlar -----

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif ✅\n/ ping, /list, /add, /remove komutlarını kullanabilirsin")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif ✅")

async def list_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ""
    for plat in ids:
        msg += f"{plat.upper()}: {', '.join(ids[plat])}\n"
    await update.message.reply_text(msg or "Henüz ID eklenmemiş.")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /add <bigo/tiktok> <ID>")
        return
    platform = context.args[0].lower()
    user_id = context.args[1]
    if platform not in ids:
        await update.message.reply_text("Platform: bigo veya tiktok olmalı")
        return
    if user_id not in ids[platform]:
        ids[platform].append(user_id)
        save_ids()
    await update.message.reply_text(f"{platform.upper()} ID’leri: {', '.join(ids[platform])}")

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /remove <bigo/tiktok> <ID>")
        return
    platform = context.args[0].lower()
    user_id = context.args[1]
    if platform in ids and user_id in ids[platform]:
        ids[platform].remove(user_id)
        save_ids()
    await update.message.reply_text(f"Güncel {platform.upper()} ID’leri: {', '.join(ids[platform])}")

# ----- Uygulama başlat -----
app = ApplicationBuilder().token(TOKEN).build()

# Komut ekle
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("list", list_ids))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("remove", remove))

# Polling başlat
app.run_polling()

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif ✅")

app.add_handler(CommandHandler("ping", ping))



