import os, update, time

while True:
	try:
		update.update()
	except Exception as e:
		os.system("curl -X POST -d \"{\\\"text\\\": \\\"\\\"}\" -H \"Content-Type: application/json\" https://api.pushcut.io/LD6ePZS6z3PNXGXqHHgFU/notifications/KadroError")
	finally:
		time.sleep(3600)	