import os
import json
from flask import Flask, request
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
from jinja2 import Template

app = Flask(__name__)

# Get token from environment variable
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

async def send_telegram_message(message_str):
    bot = Bot(token=bot_token)
    await bot.send_message(
        chat_id=chat_id,
        text=message_str,
        parse_mode=ParseMode.HTML
    )

async def send_telegram_document(message_str, html_str):
    bot = Bot(token=bot_token)
    await bot.send_document(
        chat_id=chat_id,
        document=html_str.encode('utf-8'),
        filename='email.html',
        caption=message_str,
        parse_mode=ParseMode.HTML
    )

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.form.get('mail')
        json_data = json.loads(data)
        print(json.dumps(json_data, indent=4), flush=True)

        # Template is in templates/message.j2
        with open('templates/message.j2', 'r') as template_file:
            template_content = template_file.read()

        # Create a Jinja2 template
        template = Template(template_content)

        # Generate message string using the template
        message_str = template.render(
            json_data=json_data,
        )
        print(message_str, flush=True)

        # Send the message to Telegram
        if json_data.get('html'):
            html_str = json_data['html']
            asyncio.run(send_telegram_document(message_str, html_str))
        else:
            asyncio.run(send_telegram_message(message_str))

    except Exception as e:
        # Send raw data to Telegram if there's an error
        error_message = f"SMTP2Telegram\nError: {str(e)}\n\nData: {request.data.decode()}"
        print(error_message, flush=True)
        asyncio.run(send_telegram_message(error_message))

    return "OK", 200

if __name__ == '__main__':
    print("Starting Flask app...", flush=True)
    app.run(host='0.0.0.0', port=5000)