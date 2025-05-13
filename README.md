# gencon-events-slack-bot

A simple Slack bot that enhances unfurls for Gen Con event links by providing detailed event information.

## Features

- Automatically detects shared Gen Con event links in Slack.
- Fetches event details such as title, start time, duration, and cost from a preloaded dataset.
- Displays event information in a user-friendly format directly in Slack.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/gencon-events-slack-bot.git
   cd gencon-events-slack-bot
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   - `SLACK_CLIENT_ID`
   - `SLACK_CLIENT_SECRET`
   - `SLACK_SIGNING_SECRET`
   - `PORT` (optional, defaults to `3000`)

4. Run the bot:
   ```bash
   poetry run python app.py
   ```

## Data Updates

- The bot periodically fetches the latest `events.xlsx` file from Gen Con's website every 6 hours.
- The data is stored in the `data/` directory.

## Requirements

- Python 3.11+
- Poetry
- Slack API credentials

## Contributing

Feel free to submit issues or pull requests to improve the bot.

## License

This project is licensed under the MIT License.
