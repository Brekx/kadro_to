import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar']

def getService():
  creds = None
  if not os.path.exists('token.json'):
    raise Exception("No token")
  creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  return build('calendar', 'v3', credentials=creds)

def getList(service) -> list:
  tmp_list = service.calendarList().list().execute()
  calList = tmp_list['items']
  while 'nextPageToken' in tmp_list:
    tmp_list = service.calendarList().list(pageToken=tmp_list['nextPageToken']).execute()
    calList += tmp_list['items']
  return calList