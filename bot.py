from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp as youtube_dl
import os

TOKEN = '7252779471:AAF6zpHOJm4PjIcv8qNQV11Ey74j8wqeOXA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً! أرسل لي رابط فيديو من تيك توك، إنستجرام، أو تويتر لتحميله.')

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
    if "tiktok.com" in url or "instagram.com" in url or "x.com" in url:
        try:
            video_file = download_video(url)
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(video_file)  # احذف الملف بعد الإرسال لتوفير المساحة
        except Exception as e:
            await update.message.reply_text('فشل في تحميل الفيديو. الرجاء التحقق من الرابط والمحاولة مرة أخرى.')
            print(f"Error: {e}")
    else:
        await update.message.reply_text('الرجاء إرسال رابط فيديو من تيك توك، إنستجرام، أو تويتر.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
