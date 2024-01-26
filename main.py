import os
import requests
import schedule
import time
import json
from datetime import datetime, timedelta, timezone
# Read Slack webhook URLs from environment variables
CHANNEL_1_WEBHOOK_URL = os.environ.get('CHANNEL_1_WEBHOOK_URL')
CHANNEL_2_WEBHOOK_URL = os.environ.get('CHANNEL_2_WEBHOOK_URL')

# Central Standard Time (CST) timezone
CST = timezone(timedelta(hours=-6))

# Global variable to track if Channel 2 message was sent today
channel_2_sent_today = False

def send_slack_message(webhook_url, message):
    payload = {
        'text': message
    }
    requests.post(webhook_url, json=payload)

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

def send_messages():
    # Send message to channel 1 every 15 minutes
    send_slack_message(CHANNEL_1_WEBHOOK_URL, 'Message to Channel 1 - Every 15 minutes')

    # Send message to channel 2 at 11:00am CST every day if not sent today
    now_cst = datetime.now(CST)
    if now_cst.hour == 11 and now_cst.minute == 0 and not channel_2_sent_today:
        quote_of_the_day = get_quote()
        send_slack_message(CHANNEL_2_WEBHOOK_URL, f'Message to Channel 2 - 11:00am CST: {quote_of_the_day}')
        # Set the flag to indicate that Channel 2 message was sent today
        channel_2_sent_today = True

def send_backup_message():
    # Send backup message to channel 2 at 12:00pm CST if the original message wasn't sent at 11:00am
    now_cst = datetime.now(CST)
    if now_cst.hour == 12 and not channel_2_sent_today:
        send_slack_message(CHANNEL_2_WEBHOOK_URL, 'Backup Message to Channel 2')

if __name__ == "__main__":
    # Schedule the task to run every minute
    schedule.every().minute.do(send_messages)

    # Schedule the backup message task to run once a day at 12:00pm CST
    schedule.every().day.at("12:00").do(send_backup_message)

    while True:
        schedule.run_pending()
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
