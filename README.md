# SMTP2Telegram 📧➡️📱

A lightweight SMTP server that forwards incoming emails to Telegram. Designed to run in Docker for easy deployment.

Uses a containerized version of [ehlo](https://github.com/ehlo-io/ehlo).

## Prerequisites 📋

- Docker and Docker Compose installed
- Telegram bot token (from [@BotFather](https://t.me/BotFather))
- Telegram chat ID where messages should be forwarded

## Quick Start 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/felixkohlhas/smtp2telegram.git
   cd smtp2telegram
   ```

2. Copy and configure the example file:
   ```bash
   cp docker-compose.example.yml docker-compose.yml
   nano docker-compose.yml  # or edit with your preferred editor
   ```

3. Set your Telegram credentials:
   ```yaml
   environment:
     TELEGRAM_BOT_TOKEN: "your_bot_token_here"
     TELEGRAM_CHAT_ID: "your_chat_id_here"
   ```

4. Build and run the container:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

## Configuration ⚙️

### Environment Variables

| Variable            | Description                          | Required |
|---------------------|--------------------------------------|----------|
| `TELEGRAM_BOT_TOKEN`| Your Telegram bot token             | Yes      |
| `TELEGRAM_CHAT_ID`  | Target chat/channel/group ID        | Yes      |

### Ports

- SMTP port (default: 10025) - ensure this is accessible and not blocked

## Usage Example 💡

Configure your email client or application to send emails to:
- Server: IP/hostname where SMTP2Telegram is running
- Port: 10025 (or your custom port)
- No authentication required

All received emails will be forwarded to your specified Telegram chat.