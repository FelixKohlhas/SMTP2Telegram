import os
import json
from flask import Flask, request
from telegram import Bot
from telegram.constants import ParseMode
import asyncio
import bleach
from html import escape

app = Flask(__name__)

template = """
<b>SMTP2Telegram</b>
Date: {date}
Subject: {subject}

{content}
"""

# Get token from environment variable
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')

async def send_telegram_message(message):
    bot = Bot(token=bot_token)
    await bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML
    )

def sanitize_html_for_telegram(unsafe_html):
    # Telegram supports a limited subset of HTML tags
    allowed_tags = [
        'b', 'strong',        # bold
        'i', 'em',            # italic
        'u', 'ins',           # underline
        's', 'strike', 'del', # strikethrough
        'a',                  # links
        'code',               # monospace
        'pre'                 # code blocks
    ]
    
    allowed_attributes = {
        'a': ['href']  # only allow href attributes for links
    }
    
    # First escape everything, then parse allowed tags
    sanitized = bleach.clean(
        unsafe_html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
        strip_comments=True
    )
    
    # Ensure any remaining HTML entities are properly escaped
    sanitized = escape(sanitized)
    
    return sanitized

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.form.get('mail')
        json_data = json.loads(data)
        print(json.dumps(json_data, indent=4), flush=True)

        if json_data.get('text'):
            content = json_data['text']
        else:
            content = sanitize_html_for_telegram(json_data['html'])

        message_str = template.format(
            date=json_data['date'],
            subject=json_data['subject'],
            content=content
        )
        print(message_str, flush=True)

        # Send the message to Telegram
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