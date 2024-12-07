import asyncio
import os
import pathlib
import signal
import sys
import socket
import logging
import re
import argparse
from string import Template
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

# Constants
TELEGRAM_MAX_TEXT_SIZE = 4096
BOT_TOKEN = os.getenv("LOG2TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("LOG2TELEGRAM_CHAT_ID")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize the Telegram bot
if not BOT_TOKEN or not CHAT_ID:
    logger.error("🚫 LOG2TELEGRAM_BOT_TOKEN and LOG2TELEGRAM_CHAT_ID must be set in the .env file.")
    sys.exit(1)

bot = Bot(token=BOT_TOKEN)

# Welcome message template
WELCOME_TEXT_TEMPLATE = Template('''
<b>👋 Monitoring started for the next file on the host:</b>

Host: ${hostname}
File: ${path}

File contains [${line_count}] lines; here are the latest lines:
${displayed_lines}
''')

MAX_DISPLAY_LINES = 4  # Limit on lines to display in welcome message
MAX_TELEGRAM_MESSAGE_LEN = 4081  # Max message length for Telegram with buffer


async def get_hostname() -> str:
    """Retrieve the hostname of the current machine."""
    try:
        hostname = socket.gethostname()
    except Exception as e:
        logger.error(f"Error retrieving hostname: {e}")
        hostname = "unknown_host"
    return hostname


async def send_message(text: str):
    """Send a message to the specified Telegram chat."""
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')


def get_formatted_lines(lines: list) -> str:
    """Format lines for better display in Telegram messages."""
    f_lines = ['...', '...'] + lines[-3:]

    f_lines = [f"║ {line.strip()}" for line in f_lines] + ['╚' + '═' * 24]
    f_lines = [line[:20] for line in f_lines]
    return '\n'.join(f_lines)


async def send_welcome(path: pathlib.Path, lines: list):
    """Send an initial welcome message when monitoring starts."""
    welcome_text = WELCOME_TEXT_TEMPLATE.substitute(
        hostname=await get_hostname(),
        path=path.resolve().as_posix(),
        line_count=len(lines),
        displayed_lines=get_formatted_lines(lines))
    await send_message(welcome_text)

def get_file_modified_time(path: pathlib.Path) -> float:
    """Return the last modified timestamp of the file or 0 if unavailable."""
    if not path.exists():
        return 0
    try:
        return path.stat().st_mtime
    except Exception as e:
        logger.error(f"Unable to retrieve modified time for file '{path}': {e}")
        return 0

def filter_color_codes(line: str) -> str:
    """Remove ANSI color codes from a line."""
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def filter_timestamps(line: str) -> str:
    """Remove timestamps at the start of the line in various formats."""
    # This regex matches:
    # - "HH:MM", "HH:MM:SS", "HH:MM:SS,SSS"
    # - "YYYY-MM-DD HH:MM:SS", "YYYY-MM-DD HH:MM:SS,SSS"
    return re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})?|\d{1,2}:\d{2}(?::\d{2})?(?:,\d{3})?\s*',
                  '', line)


async def read_file_from_position(path: pathlib.Path, position: int = 0):
    """Read new lines from the file starting from a specified position."""
    if not path.is_file() or not os.access(path, os.R_OK):
        logger.error(f"File '{path}' cannot be read. Check permissions.")
        return [], -1  # Return -1 to indicate a read error

    try:
        with path.open('r') as file:
            file.seek(position)
            lines = file.readlines()
            new_position = file.tell()
    except Exception as e:
        logger.error(f"Error reading file '{path}': {e}")
        return [], -1  # Return -1 on read error
    return lines, new_position


async def send_lines(lines: list, filter_color: bool = False, filter_timestamp: bool = False):
    """Send lines to Telegram, trimming if the message exceeds the maximum allowed length."""
    if filter_color:
        lines = [filter_color_codes(line) for line in lines]
    if filter_timestamp:
        lines = [filter_timestamps(line) for line in lines]

    lines = [line.lstrip(" -") for line in lines]

    message = '\n'.join(lines)
    if len(message) > MAX_TELEGRAM_MESSAGE_LEN:
        message = message[:MAX_TELEGRAM_MESSAGE_LEN] + '\n...\n⚔️ Message trimmed'
    await send_message(message)


async def monitor_file(path: pathlib.Path, seconds_delay: int, filter_color: bool, filter_timestamp: bool):
    """Monitor a file for changes, sending new content to Telegram."""
    await asyncio.sleep(2)

    lines, position = await read_file_from_position(path)
    if position == -1:
        logger.error("Failed to read the file initially. Exiting monitoring.")
        return

    await send_welcome(path, lines)

    last_modified_time = get_file_modified_time(path)

    while True:
        await asyncio.sleep(seconds_delay)

        current_modified_time = get_file_modified_time(path)
        if current_modified_time == last_modified_time:
            continue  # No changes detected

        last_modified_time = current_modified_time
        lines, new_position = await read_file_from_position(path, position)
        if position == -1:
            continue

        if lines:
            await send_lines(lines, filter_color, filter_timestamp)
            position = max(position, new_position)
        else:
            logger.info("No new lines to send.")


def handle_suspend(signal, frame):
    """Handle the SIGTSTP signal (Ctrl+Z)."""
    logger.info("Process suspended. Exiting...")
    # No need to pause manually; the system handles the suspension
    sys.exit(0)


def handle_interrupt(signal, frame):
    """Handle the SIGINT signal (Ctrl+C)."""
    logger.info("Process interrupted by user. Exiting...")
    sys.exit(0)


def main():
    signal.signal(signal.SIGTSTP, handle_suspend)
    signal.signal(signal.SIGINT, handle_interrupt)
    logger.info("Running ... Press Ctrl+C to stop or Ctrl+Z to suspend.")

    """Parse arguments, validate environment, and start file monitoring."""
    parser = argparse.ArgumentParser(description="Monitor a file for changes and send updates to Telegram.")
    parser.add_argument("path", type=pathlib.Path, help="Path to the file to monitor.")
    parser.add_argument("--delay", type=int, default=1,
                        help="Polling interval in seconds (default: 1). Must be positive.")
    parser.add_argument("--filter-color-chars", action="store_true",
                        help="Remove ANSI color codes from lines before sending.")
    parser.add_argument("--filter-timestamps", action="store_true",
                        help="Remove timestamps at the start of lines before sending.")
    args = parser.parse_args()

    # Validate seconds_delay argument
    if args.delay < 1:
        logger.error("🚫 --delay must be at least 1 second.")
        sys.exit(1)

    # Validate the file exists and is readable
    if not args.path.exists():
        logger.error(f"🚫 The file '{args.path}' does not exist.")
        sys.exit(1)
    if not os.access(args.path, os.R_OK):
        logger.error(f"🚫 The file '{args.path}' is not readable. Check permissions.")
        sys.exit(1)

    # Start monitoring
    asyncio.run(monitor_file(args.path, args.delay, args.filter_color_chars, args.filter_timestamps))


if __name__ == "__main__":
    main()
