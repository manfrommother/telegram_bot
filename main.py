import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class JffBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self.trigger_words = [
            'челси', 'NDF', 'Доминион', 'Доминион 90', 'Айсберг', 'Звезда',
            'Нация', 'ЗН', 'Империал', 'Импульс', 'особый статут', 'Орион',
            'Орбита', 'Скиф', 'Сокол'
        ]

    async def start_command(self, update: Update, context: CallbackContext) -> None:
        await update.message.reply_text('Привет! Я бот команды JFF.')

    async def handle_message(self, update: Update, context: CallbackContext) -> None:
        message_text = update.message.text.lower()
        if any(word.lower() in message_text for word in self.trigger_words):
            if update.message.is_topic_message:
                thread_id = update.message.message_thread_id
                await update.message.reply_text('***', message_thread_id=thread_id)
                logging.info(f'Ответ в треде: {thread_id}')
            else:
                await update.message.reply_text('***')
                logging.info('Ответ не в треде')

    def run(self) -> None:
        self.application.add_handler(CommandHandler("start", self.start_command))

        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        self.application.run_polling()

    async def restart(self):
        while True:
            try:
                await self.run()
            except Exception as e:
                logging.error(f"Error during bot execution: {e}")
                logging.info("Restarting bot in 5 seconds...")
                await asyncio.sleep(5)

if __name__ == '__main__':
    TOKEN = '***'
    bot = JffBot(TOKEN)
    bot.run()

