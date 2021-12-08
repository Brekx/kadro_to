from webbrowser import get
from Employer import Employee
import gAcces
from datetime import date, datetime, timedelta
from kadrometr_html import getShifts


s = gAcces.getService()

start = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 2, 0, 0)
end = start + timedelta(14)
kadr = getShifts(start, end)
calList = gAcces.getList(s)


for person in calList:
  name = person['summary']
  id = person['id']
  try:
    emp = Employee(s, name, id = id)
    print("For " + emp.name, end="")
    emp.getGoogleShifts(start, end)
    emp.getKadroShifts(kadr)
    emp.diff()
    print(" need to resolve " + str(len(emp.toAdd) + len(emp.toRemove)) + " changes ", end="")
    emp.resolveChanges()
    print("...resolved")
  except Exception as e:
    print(e.args)