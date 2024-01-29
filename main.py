import os
import requests
import schedule
import time
import json
from datetime import datetime, timedelta, timezone
# Read Slack webhook URLs from environment variables
CHANNEL_1_WEBHOOK_URL = os.environ.get('TEST_WEBHOOK_URL')
CHANNEL_2_WEBHOOK_URL = os.environ.get('QUOTE_WEBHOOK_URL')

# Read Slack webhook URL from environment variable
#SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL')

# Central Standard Time (CST) timezone
CST = timezone(timedelta(hours=-6))
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def send_slack_message(message):
    payload = {'text': message}
    requests.post(CHANNEL_1_WEBHOOK_URL, json=payload)

def send_daily_message():
    now_cst = datetime.now(CST)
    if now_cst.hour == 11 and now_cst.minute == 0:
        send_slack_message(get_quote())

def send_uptime_message():
    now_cst = datetime.now(CST)
    payload = {'text': now_cst}
    requests.post(CHANNEL_1_WEBHOOK_URL, json=payload)



print("finally")
# Schedule the task to run every minute
schedule.every().minute.do(send_daily_message)
schedule.every(15).minutes.do(send_uptime_message)
while True:
    schedule.run_pending()

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
