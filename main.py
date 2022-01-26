import os, update, time, datetime

while True:
	try:
		update.update()
		os.system("echo \"Succesful synch" + time.strftime("%H:%M:%S, %d.%m.%Y") +  "\" >> ~/kadro.log")
	except Exception as e:
		errorMessage = "Error in " + str(e) + " at " + time.strftime("%H:%M:%S, %d.%m.%Y")
		print(errorMessage)
		os.system("echo \" " + errorMessage + "\" >> ~/kadro.log")
		os.system("curl -X POST -d \"{\\\"text\\\": \\\"\\\"}\" -H \"Content-Type: application/json\" https://api.pushcut.io/LD6ePZS6z3PNXGXqHHgFU/notifications/KadroError")
	finally:
		now = datetime.datetime.now()
		next_hour = datetime.datetime(now.year, now.month, now.day if now.hour/24<1 else now.day+1 , (now.hour+1)%24, 0, 0)
		remaining = next_hour - now
		time.sleep(remaining.seconds - 300)