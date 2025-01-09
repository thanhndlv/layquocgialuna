from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import requests

# Token bot Telegram
TELEGRAM_TOKEN = "7815560131:AAEeaHW-GM-6XJM_JFSobUA-wTOiY6w-mgU"  # Thay bằng token của bot


# Hàm gọi API để lấy dữ liệu IP
def get_ip_by_country(countries):
    regions = ",".join(countries)
    api_url = f"https://tq.lunaproxy.com/getflowip?neek=1501384&num=3&regions={regions}&ip_si=1&level=1&sb="
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Lỗi khi gọi API: {response.status_code}"


# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Chào mừng bạn! Hãy nhập mã quốc gia (ví dụ: IN,US,VN) để lấy dữ liệu IP."
    )


# Hàm xử lý tin nhắn từ người dùng
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text.strip()
    countries = [code.strip().upper() for code in user_input.split(",")]
    ip_data = get_ip_by_country(countries)

    if "Lỗi" not in ip_data:
        await update.message.reply_text(f"Dữ liệu từ các nước ({', '.join(countries)}):\n{ip_data}")
    else:
        await update.message.reply_text(ip_data)


# Hàm xử lý lỗi
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Có lỗi xảy ra, vui lòng thử lại sau.")


# Main function để chạy bot
def main():
    # Tạo ứng dụng bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Chạy bot
    application.run_polling()


if __name__ == "__main__":
    main()
