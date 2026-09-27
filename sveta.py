import os
import telebot

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "ВСТАВЬ_СВОЙ_ТОКЕН_ОТ_BOTFATHER"
SAVE_DIR = "saved_media"
# =====================

os.makedirs(SAVE_DIR, exist_ok=True)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def cmd_start(msg):
    bot.reply_to(msg, "Привет! Отправь фото, кружок, голосовое или видео — сохраню.")


@bot.message_handler(content_types=["photo", "video_note", "voice", "video", "audio", "document"])
def save_media(msg):
    try:
        fid = None
        ext = "bin"

        if msg.photo:
            fid = msg.photo[-1].file_id
            ext = "jpg"
        elif msg.video_note:
            fid = msg.video_note.file_id
            ext = "mp4"
        elif msg.voice:
            fid = msg.voice.file_id
            ext = "ogg"
        elif msg.video:
            fid = msg.video.file_id
            ext = "mp4"
        elif msg.audio:
            fid = msg.audio.file_id
            ext = "mp3"
        elif msg.document:
            fid = msg.document.file_id
            ext = "bin"

        if not fid:
            return

        info = bot.get_file(fid)
        data = bot.download_file(info.file_path)

        path = os.path.join(SAVE_DIR, f"{msg.message_id}.{ext}")
        with open(path, "wb") as f:
            f.write(data)

        bot.reply_to(msg, f"✅ Сохранил: {path}")

    except Exception as e:
        bot.reply_to(msg, f"❌ Ошибка: {e}")


if __name__ == "__main__":
    print("Бот запущен... Ctrl+C для остановки")
    bot.infinity_polling()
