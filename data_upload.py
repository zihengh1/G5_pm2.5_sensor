import time
import datetime
import os
import httplib, urllib
import g3

air = g3.g3sensor()

while True:
		try:
				pmdata = air.read("/dev/ttyAMA0")
				
		except:
				pmdata=[0,0,0,0,0,0]

		print "pm1 : %d" %pmdata[3]
		print "pm10 : %d" %pmdata[4]
		print "pm2.5 : %d" %pmdata[5]

		# thingspeak
		params = urllib.urlencode({'field1': pmdata[3], 'field2': pmdata[4], 'field3': pmdata[5], 'key':'YAFYMHZWAA33M2PG'})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		try:
				tconn = httplib.HTTPConnection("api.thingspeak.com:80")
				tconn.request("POST", "/update", params, headers)
				response = tconn.getresponse()
				data = response.read()
				tconn.close()
    except:
        continue
				time.sleep(600)


