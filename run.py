import asyncio
import schedule
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import requests

from parse import parse_seat

import nest_asyncio
nest_asyncio.apply()


BOT_TOKEN = os.environ.get('BOT_TOKEN')

chat_mass = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_mass.append(update.effective_chat.id)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


def sendmess():
    seat = parse_seat()
    txt = f"Свободных мест: {seat}"

    for chat_id in chat_mass:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={txt}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to send message. Status code: {response.status_code}\n{response.text}")


async def schedule_runner():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    # Создаем Telegram-бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Добавляем задачу в расписание
    schedule.every(1).minutes.do(sendmess)

    # Запускаем шедулер в фоновом режиме
    asyncio.create_task(schedule_runner())

    # Запускаем Telegram-бота
    print("Starting bot...")
    await app.run_polling()


# Запуск для сред с работающим event loop
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(main())
