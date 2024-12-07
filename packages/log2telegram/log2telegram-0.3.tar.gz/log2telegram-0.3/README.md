# log2telegram

log2telegram is a CLI tool to monitor changes in a specified log file and send updates to a Telegram chat. This package allows you to stay informed about updates in critical logs or other files by sending new content as Telegram messages, with customizable options to filter color codes and timestamps.

Features

	•	Real-Time Monitoring: Continuously watches for changes in a log file, sending new content as Telegram messages.
	•	Configurable Delay: Set a custom interval for checking the file for changes.
	•	Filtering Options: Remove ANSI color codes and timestamps at the start of lines for cleaner messages.
	•	Customizable Message Splitting: Automatically splits messages if they exceed the Telegram message size limit.
	•	Error Handling and Logging: Logs errors if the file is unreadable, ensuring smooth operation and easy debugging.

Installation

You can install the package via PyPI:

pip install log2telegram

Setup

To use log2telegram, add the following environment variables to a .env file:

LOG2TELEGRAM_BOT_TOKEN=<your-telegram-bot-token>
LOG2TELEGRAM_CHAT_ID=<your-chat-id>

	•	LOG2TELEGRAM_BOT_TOKEN: Your Telegram bot token, obtained from BotFather.
	•	LOG2TELEGRAM_CHAT_ID: The chat ID where messages will be sent.

Usage

Run the log2telegram command to monitor a file for changes. You can specify the path to the file and set optional flags for filtering.

Command-Line Arguments

log2telegram <file-path> [--seconds_delay SECONDS] [--filter-color-chars] [--filter-timestamps]

	•	<file-path> (required): The path to the file to monitor.
	•	--seconds_delay (optional): Interval in seconds between each check (default: 1). Must be a positive integer.
	•	--filter-color-chars (optional): Removes ANSI color codes from lines before sending.
	•	--filter-timestamps (optional): Removes timestamps at the start of lines.

Examples

	1.	Basic Usage
Monitor a log file with a default polling delay of 1 second.

Example Workflow

	1.	Start the program to monitor the specified file.
	2.	Upon changes, new content is sent to the designated Telegram chat.
	3.	If specified, color codes and timestamps are removed from each line before sending.

Requirements

	•	Python 3.7+
	•	Dependencies managed automatically upon installation.

License

This package is licensed under the MIT License.

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements.