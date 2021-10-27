from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
SCOPES = "https://www.googleapis.com/auth/calendar"

with open("savings.json", 'r') as inputfile:
  try:
    base = json.load(inputfile)
  except:
    base = {}
creds = None
if os.path.exists('token.json'):
  creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
      'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
  with open('token.json', 'w') as token:
    token.write(creds.to_json())
service = build('calendar', 'v3', credentials=creds)

def checkIfCalendarExist(name, calList) -> int:
  for cal in calList['items']:
    if cal['summary'] == name:
      return calList['items'].index(cal)
  return 0

def getCalendars():
  import kadrometr_html
  kardCal = kadrometr_html.getNextWeekCalendar()
  calList1 = service.calendarList().list().execute()
  calList2 = service.calendarList().list(pageToken=calList1['nextPageToken']).execute()["items"]
  calList1 = calList1['items']
  calList = calList1 + calList2
  return [kardCal, {'items': calList}]


def addCalendars():  
  import time, datetime, kadrometr_html
  calendars = getCalendars()
  kardCal = calendars[0]
  calList = calendars[1]
  num = 0
  for i in list(kardCal.keys()):
    name = kardCal[i]['name']
    num += 1
    if checkIfCalendarExist(name, calList):
      print("skipping " + str(num))
      continue
    print(name)
    calendar = {
      'summary': name,
      'timeZone': 'Europe/Warsaw'
    }
    succeed = False
    while(not succeed):
      try:
        created_calendar = service.calendars().insert(body=calendar).execute()
        # print("creale calendar" + name)
        # calendar_info = {"name":name, 'id':created_calendar['id']}
        succeed = True
        print("Waiting 5 min " + datetime.datetime.now().strftime("%H:%M"))
        time.sleep(300)
      except Exception as e:
        calendar_info = {}
        print(e)
        print("Sleeping for 10min added " + str(num) + " " + datetime.datetime.now().strftime("%H:%M"))
        time.sleep(600)
    
    # base['calendars_info'].append(calendar_info)

addCalendars()