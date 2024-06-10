from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp as youtube_dl
import os



TOKEN = '7252779471:AAF6zpHOJm4PjIcv8qNQV11Ey74j8wqeOXA'  # تأكد من وضع التوكن الصحيح هنا

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'حياك الله اخي المحارب ارسل الرابط للبداء ⚔️\nيمكنك إرسال روابط تيك توك، يوتيوب، إنستجرام أو تويتر واختيار الجودة المطلوبة (مثل 720p) أو دعها فارغة للحصول على الجودة الافضل.')

def download_video(url, quality=None):
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'merge_output_format': 'mp4',
        'nocheckcertificate': True  # تعطيل التحقق من الشهادات SSL
    }

    if quality:
        ydl_opts['format'] = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)

    return video_filename

def save_downloaded_url(url):
    with open("downloaded_urls.txt", "a") as file:
        file.write(url + "\n")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.split()
    url = message[0]
    quality = None
    if len(message) > 1:
        quality = message[1]

    supported_sites = ["tiktok.com", "youtube.com", "youtu.be", "instagram.com", "x.com"]

    if any(site in url for site in supported_sites):
        try:
            video_file = download_video(url, quality)
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(video_file)  # احذف الملف بعد الإرسال لتوفير المساحة
            save_downloaded_url(url)  # سجل الرابط في الملف
        except Exception as e:
            await update.message.reply_text('يوجد مشكلة نعتذر أية المحارب 😞.')
            print(f"Error: {e}")
    else:
        await update.message.reply_text('فقط روابط تيك توك، يوتيوب، إنستجرام وتويتر ✋🏻')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
