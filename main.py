import os
import slack_sdk
from flask import Flask
from keep_alive import keep_alive
import requests
import json
import schedule
import time as tim
from datetime import time, timedelta, datetime, date

slackToken = os.environ.get('slackToken')
#keep_alive has to come before the client server
keep_alive()
client = slack_sdk.WebClient(slackToken)


'''def alive_check():
  client.chat_postMessage(channel='bot-testing', text=get_quote())
'''

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)

print(get_quote)
'''
def post_RealMessage():
  client.chat_postMessage(channel='#kairo-motivational-corner',
                          text=get_quote())
  #log that we posted the message on this date
  str = datetime.strftime(date.today(), "%m/%d/%Y")
  print("posting real message: " + str)
  #File_Object2 = open("lastRunDate.txt", "w")
  #File_Object2.write(str)
  #File_Object2.close()


def checkIfMessageWasPosted():
  #open last run date file so we can store the last date we ran the project
  File_Object = open("lastRunDate.txt", "r")
  lastRunDate = File_Object.read()
  File_Object.close

  #if the last run date is not equal to the current day, then we have to do additional checks
  if lastRunDate != datetime.strftime(date.today(), "%m/%d/%Y"):
    #since we made it here, we know that there hasn't been a message today.
    #but, maybe there wasn't a message today because it's not noon yet

    #declare a datetime object that will be use to check what hour it in in the if statement following this
    dt = datetime.now()

    #check if it's after noon for the message
    if dt.hour > 16:
      str = datetime.strftime(date.today(), "%m/%d/%Y")
      print("posting recovery message: " + str)
      post_RealMessage()
  else:
    print("made it into else")


def post_TestMessage():
  timecheck = "Uptime check: " + datetime.strftime(datetime.now(), "%m/%d/%Y")
  client.chat_postMessage(channel='bot-testing', text=timecheck)
  print("posting Test message: " + timecheck)

#schedule.every().saturday.at("00:40").do(post_SpookyMessage)
schedule.every().day.at("16:00").do(post_RealMessage)
#schedule.every(1).minute.do(checkIfMessageWasPosted)
#schedule.every(15).minutes.do(post_TestMessage)
post_TestMessage()
while True:
  schedule.run_pending()
  tim.sleep(1)
'''
