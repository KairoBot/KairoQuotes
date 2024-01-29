import os
import requests
import schedule
import time
import json
from datetime import datetime, timedelta, timezone

# Read Slack webhook URLs from environment variables
SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')  # Channel for daily message
UPTIME_SLACK_WEBHOOK_URL = os.environ.get('UPTIME_SLACK_WEBHOOK_URL')  # Channel for uptime messages

# Central Standard Time (CST) timezone
CST = timezone(timedelta(hours=-6))
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def send_slack_message(webhook_url, message):
    payload = {'text': message}
    requests.post(webhook_url, json=payload)

def get_daily_message():
    now_cst = datetime.now(CST)
    if now_cst.hour == 11 and now_cst.minute == 0:
        return 'Daily message at 11:00am CST'

    return None

def get_uptime_message():
    now_minute = datetime.now().minute
    if now_minute % 15 == 0:
        return f'Uptime message at {now_minute} minute mark on the hour'

    return None

if __name__ == "__main__":
    # Run the scheduled tasks every minute
    while True:
        daily_message = get_daily_message()
        uptime_message = get_uptime_message()

        if daily_message:
            send_slack_message(SLACK_WEBHOOK_URL, daily_message)

        if uptime_message:
            send_slack_message(UPTIME_SLACK_WEBHOOK_URL, uptime_message)

        time.sleep(1)
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
