from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp as youtube_dl
import os

TOKEN = '7252779471:AAF6zpHOJm4PjIcv8qNQV11Ey74j8wqeOXA'  # تأكد من وضع التوكن الصحيح هنا

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('حياك الله اخي المحارب ارسل الرابط للبداء ⚔️')

def download_video(url):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True  # تعطيل التحقق من الشهادات SSL
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)
    return video_filename

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if any(site in url for site in ["tiktok.com", "instagram.com", "x.com", "youtube.com", "youtu.be"]):
        try:
            video_file = download_video(url)
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(video_file)  # احذف الملف بعد الإرسال لتوفير المساحة
        except Exception as e:
            await update.message.reply_text('يوجد مشكلة نعتذر أية المحارب 😞.')
            print(f"Error: {e}")
    else:
        await update.message.reply_text('فقط تيك توك، إنستجرام، تويتر، أو يوتيوب.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
