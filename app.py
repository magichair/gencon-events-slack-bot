import os
import re
import requests
import logging
import threading
import time
from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from events import Event

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=["links:read", "links:write"],
    installation_store=FileInstallationStore(base_dir="./data/installations"),
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data/states")
)

app = App(
    oauth_settings=oauth_settings,
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

events = dict()

@app.event("link_shared")
def unfurl_links(client, event):
    logger.info(f"Received link_shared event: {event}")
    if event is None or event.get("links") is None:
        return

    links = event.get("links")
    unfurls = {}

    for link in links:
        url = link.get("url")
        logger.info(f"Processing link: {url}")
        if not url or not re.match(r"https?://(www\.)?gencon\.com/events/\d+/?", url):
            continue

        # Extract event ID from the URL
        event_id_match = re.search(r"/events/(\d+)/?", url)
        event_id = event_id_match.group(1) if event_id_match else None
        if not event_id or event_id not in events:
            logger.warning(f"Event ID {event_id} not found in events dictionary.")
            continue

        # Retrieve event details from the events dictionary
        event_obj = events[event_id]
        title = event_obj.title
        # short_description = event_obj.short_description
        start_date_time = event_obj.start_datetime
        duration = event_obj.duration
        # location = event_obj.location
        cost = event_obj.cost

        logger.info(f"Fetched event details for Event ID: {event_id}")

        # Prepare the unfurl payload
        unfurls[url] = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<{url}|*{title}*> ({event_id})\n*Time:* {start_date_time} for {duration}\n*Cost:* {cost}"
                    }
                }
            ]
        }

    # Send the unfurl request
    if unfurls:
        client.chat_unfurl(channel=event.get("channel"), ts=event.get("message_ts"), unfurls=unfurls)

def update_events():
    global events
    while True:
        try:
            logger.info("Fetching the latest events.xlsx file...")
            response = requests.get("https://www.gencon.com/downloads/events.xlsx")
            if response.status_code == 200:
                with open("data/events.xlsx", "wb") as file:
                    file.write(response.content)
                logger.info("Successfully updated events.xlsx file.")
                events = Event.load_events("data/events.xlsx")
                logger.info("Reloaded events dictionary with the latest data.")
            else:
                logger.warning(f"Failed to fetch events.xlsx. Status code: {response.status_code}")
        except Exception as e:
            logger.error(f"Error while updating events: {e}")
        time.sleep(6 * 60 * 60)  # Wait for 6 hours

# Start the background task
threading.Thread(target=update_events, daemon=True).start()

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))