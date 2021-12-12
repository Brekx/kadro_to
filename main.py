import os, update, time

while True:
	try:
		update.update()
		os.system("echo \"Succesful synch" + time.strftime("%H:%M:%S, %d.%m.%Y") +  "\" >> kadro.log")
	except Exception as e:
		os.system("echo \" " + str(e) + "\" >> kadro.log")
		os.system("curl -X POST -d \"{\\\"text\\\": \\\"\\\"}\" -H \"Content-Type: application/json\" https://api.pushcut.io/LD6ePZS6z3PNXGXqHHgFU/notifications/KadroError")
	finally:
		time.sleep(3600)	