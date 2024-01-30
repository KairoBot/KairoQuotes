import os
import requests
import schedule
import time
import json
from datetime import datetime, timedelta, timezone

# Read Slack webhook URLs from environment variables
SLACK_WEBHOOK_URL = os.environ.get('QUOTE_WEBHOOK_URL')  # Channel for daily message
UPTIME_SLACK_WEBHOOK_URL = os.environ.get('TEST_SLACK_WEBHOOK_URL')  # Channel for uptime messages


# Central Standard Time (CST) timezone
CST = timezone(timedelta(hours=-6))

def send_slack_message(webhook_url, message):
    payload = {'text': message}
    requests.post(webhook_url, json=payload)

def send_daily_message():
    now_cst = datetime.now(CST)

    # Check if it's 11:00 AM CST
    if now_cst.hour == 11 and now_cst.minute == 0:
        send_slack_message(SLACK_CHANNEL_1_URL, 'Daily message at 11:00am CST')
        time.sleep(59)

def send_recurring_message():
    now_minute = datetime.now().minute

    # Check if it's a 15-minute mark on the hour
    if now_minute % 15 == 0:
        send_slack_message(SLACK_CHANNEL_2_URL, f'Recurring message at {now_minute} minute mark on the hour')
        time.sleep(59)

if __name__ == "__main__":
    # Run the scheduled tasks every minute
    while True:
        send_daily_message()
        send_recurring_message()
        time.sleep(1)  # Sleep for 60 seconds (1 minute)
'''import os
import slack_sdk
from flask import Flask
import requests
import json
import schedule
from datetime import datetime

slackToken = os.environ.get('slackToken')
client = slack_sdk.WebClient(slackToken)


def post_RealMessage():
    client.chat_postMessage(channel='#kairo-motivational-corner', text=get_quote())


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


app = Flask(__name__)


def scheduled_task():
    # Replace the following print statement with your task logic
    print("Executing task at noon EST:", datetime.now())
    post_RealMessage()


# Schedule the task to run every day at noon EST
schedule.every().day.at("12:00").do(scheduled_task)

# Flask route for testing purposes
@app.route('/')
def home():
    return 'Scheduled task is running!'


if __name__ == '__main__':
    # Run the Flask app
    app.run(port=5000)
'''
