import json
with open("savings.json", 'r') as inputfile:
  try:
    base = json.load(inputfile)
  except:
    base = {}

def getActualSchedule(dtstart, dtend):
  import urllib3
  http = urllib3.PoolManager()
  has_key = False
  for key in base.keys():
    if key == 'credentials':
      has_key = True
  if has_key:
    has_key = False
    for key in base['credentials'].keys():
      if key == 'authToken':
        has_key = True
  if not has_key or base['credentials']['authToken'] == "":
    r = http.request('POST', 'https://api.kadromierz.pl/security/authentication', fields={'email':base['credentials']['email'], 'password':base['credentials']['password']})
    base['credentials']['authToken'] = json.loads(r.data.decode('utf8').replace("'", '"'))['auth_token']
    print("Renewing auth token")
  http.headers['Authorization'] = 'AUTH-TOKEN token="' + base['credentials']['authToken'] + '"'
  start = str(dtstart.year) + '-' + str(dtstart.month) + '-' + str(dtstart.day)
  end = str(dtend.year) + '-' + str(dtend.month) + '-' + str(dtend.day)
  r = http.request('GET', 'https://api.kadromierz.pl/locations/7738/schedule?from=' + start + '&to=' + end + '&show_drafts=false')
  if r.status != 200 and r.status != 404:
    base['credentials']['authToken'] = ""
  return json.loads(r.data.decode('utf8').replace("'", '"'))

def getNextWeekCalendar():
  from datetime import datetime, timedelta
  s = datetime.today()
  e = s + timedelta(7)
  schedule_data = getActualSchedule(s, e)
  schedule = {}
  for employee in schedule_data['schedule']['employees']:
    employee_shifts = []
    for shift in employee['shifts_for_other_locations']:
      start = datetime(int(shift['start_timestamp'][0:4]), int(shift['start_timestamp'][5:7]), int(shift['start_timestamp'][8:10]), int(shift['start_timestamp'][11:13]), int(shift['start_timestamp'][14:16]), int(shift['start_timestamp'][17:19]))
      end = datetime(int(shift['end_timestamp'][0:4]), int(shift['end_timestamp'][5:7]), int(shift['end_timestamp'][8:10]), int(shift['end_timestamp'][11:13]), int(shift['end_timestamp'][14:16]), int(shift['end_timestamp'][17:19]))
      new_event = {'dtstart' : start, 'dtend' : end, 'location' : shift['job_title']['title'], 'note' : ""}
      employee_shifts.append(new_event)
    employee_record = {'name' : employee['first_name'] + ' ' + employee['last_name'], \
                        'schedule' : employee_shifts}
    schedule[employee['id']] = employee_record

  employees_to_fill = list(schedule.keys())
  for employee in range(0, len(schedule)-1): 
    employee_id = employees_to_fill.pop(0)
    for shift in schedule[employee_id]['schedule']:
      for other_employer_id in employees_to_fill:
        for other_employer_shift in schedule[other_employer_id]['schedule']:
          if( shift['location'] == other_employer_shift['location'] and \
            (( shift['dtstart'] >= other_employer_shift['dtstart'] and shift['dtstart'] < other_employer_shift['dtend']) or \
            ( shift['dtstart'] <= other_employer_shift['dtstart'] and shift['dtend'] > other_employer_shift['dtstart']))):
            note = schedule[other_employer_id]['name']
            earlier = shift['dtstart'] < other_employer_shift['dtstart']
            later = shift['dtend'] > other_employer_shift['dtend']
            if(earlier and not later):
              note += ' (od ' + other_employer_shift['dtstart'].strftime("%H:%M") + ')'
            if(earlier and later):
              note += ' (od ' + other_employer_shift['dtstart'].strftime("%H:%M") + ' do ' + other_employer_shift['dtend'].strftime("%H:%M") + ')'
            if(not earlier and later):
              note += ' (do ' + other_employer_shift['dtend'].strftime("%H:%M") + ')'
            shift['note'] += note if shift['note'] == "" else ('\n' + note)
            note = schedule[employee_id]['name']
            earlier = other_employer_shift['dtstart'] < shift['dtstart']
            later = other_employer_shift['dtend'] > shift['dtend']
            if(earlier and not later):
              note += ' (od ' + shift['dtstart'].strftime("%H:%M") + ')'
            if(earlier and later):
              note += ' (od ' + shift['dtstart'].strftime("%H:%M") + ' do ' + shift['dtend'].strftime("%H:%M") + ')'
            if(not earlier and later):
              note += ' (do ' + shift['dtend'].strftime("%H:%M") + ')'
            other_employer_shift['note'] += note if other_employer_shift['note'] == "" else ('\n' + note)

  return schedule

def getNextWeekCalendar():
  from datetime import datetime, timedelta
  s = datetime.today()
  e = s + timedelta(7)
  schedule_data = getActualSchedule(s, e)
  schedule = {}
  for employee in schedule_data['schedule']['employees']:
    employee_shifts = []
    for shift in employee['shifts_for_other_locations']:
      start = datetime(int(shift['start_timestamp'][0:4]), int(shift['start_timestamp'][5:7]), int(shift['start_timestamp'][8:10]), int(shift['start_timestamp'][11:13]), int(shift['start_timestamp'][14:16]), int(shift['start_timestamp'][17:19]))
      end = datetime(int(shift['end_timestamp'][0:4]), int(shift['end_timestamp'][5:7]), int(shift['end_timestamp'][8:10]), int(shift['end_timestamp'][11:13]), int(shift['end_timestamp'][14:16]), int(shift['end_timestamp'][17:19]))
      new_event = {'dtstart' : start, 'dtend' : end, 'location' : shift['job_title']['title'], 'note' : ""}
      employee_shifts.append(new_event)
    employee_record = {'name' : employee['first_name'] + ' ' + employee['last_name'], \
                        'schedule' : employee_shifts}
    schedule[employee['id']] = employee_record
  
  employees_to_fill = list(schedule.keys())
  for employee in range(0, len(schedule)-1): 
    employee_id = employees_to_fill.pop(0)
    for shift in schedule[employee_id]['schedule']:
      for other_employer_id in employees_to_fill:
        for other_employer_shift in schedule[other_employer_id]['schedule']:
          if( shift['location'] == other_employer_shift['location'] and \
            (( shift['dtstart'] >= other_employer_shift['dtstart'] and shift['dtstart'] < other_employer_shift['dtend']) or \
            ( shift['dtstart'] <= other_employer_shift['dtstart'] and shift['dtend'] > other_employer_shift['dtstart']))):
            note = schedule[other_employer_id]['name']
            earlier = shift['dtstart'] < other_employer_shift['dtstart']
            later = shift['dtend'] > other_employer_shift['dtend']
            if(earlier and not later):
              note += ' (od ' + other_employer_shift['dtstart'].strftime("%H:%M") + ')'
            if(earlier and later):
              note += ' (od ' + other_employer_shift['dtstart'].strftime("%H:%M") + ' do ' + other_employer_shift['dtend'].strftime("%H:%M") + ')'
            if(not earlier and later):
              note += ' (do ' + other_employer_shift['dtend'].strftime("%H:%M") + ')'
            shift['note'] += note if shift['note'] == "" else ('\n' + note)
            note = schedule[employee_id]['name']
            earlier = other_employer_shift['dtstart'] < shift['dtstart']
            later = other_employer_shift['dtend'] > shift['dtend']
            if(earlier and not later):
              note += ' (od ' + shift['dtstart'].strftime("%H:%M") + ')'
            if(earlier and later):
              note += ' (od ' + shift['dtstart'].strftime("%H:%M") + ' do ' + shift['dtend'].strftime("%H:%M") + ')'
            if(not earlier and later):
              note += ' (do ' + shift['dtend'].strftime("%H:%M") + ')'
            other_employer_shift['note'] += note if other_employer_shift['note'] == "" else ('\n' + note)

  return schedule

