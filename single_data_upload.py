#/usr/bin/python

import sys
import time
import difflib
import pigpio
import httplib
import urllib

RX=14
API_key = "YAFYMHZWAA33M2PG"

def check(new_string):
		new_list = []
		for x in new_string:
    		new_list.append(x)
		standard = ["4","2","4","d","0","0","1","c"]

		def cmp(a, b):
				# print(a)
    		# print(b)
    		return (a > b) - (a < b)

		# print(cmp(new_list[0:8],standard))
		if cmp(new_list[0:8], standard) == -1:
    		for x in range(8):
        		new_list.insert(x,standard[x])
    		print("new_list",new_list)
		return new_list
		else:
				return new_list

def bytes2hex(s):
		return "".join("{:02x}".format(c) for c in s)

def data_read(data_hex):
		pm1_cf=int(data_hex[8]+data_hex[9]+data_hex[10]+data_hex[11],16)
    pm25_cf=int(data_hex[12]+data_hex[13]+data_hex[14]+data_hex[15],16)
    pm10_cf=int(data_hex[16]+data_hex[17]+data_hex[18]+data_hex[19],16)
		pm1 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23],16)
    pm25 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27],16)
		pm10 = int(data_hex[28] + data_hex[29] + data_hex[30] + data_hex[31],16)
		return [pm1_cf, pm25_cf, pm10_cf, pm1, pm25, pm10]

def data_upload(pmdata):
		params = urllib.urlencode({'field1': pmdata[3], 'field2': pmdata[4], 'field3': pmdata[5], 'key':API_key})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
		tconn = httplib.HTTPConnection("api.thingspeak.com:80")
		tconn.request("POST", "/update", params, headers)
		response = tconn.getresponse()
		data = response.read()
		tconn.close()
		time.sleep(0.1)
	
def main():
    pi = pigpio.pi()
		# print pi.connected
    pi.set_mode(RX, pigpio.INPUT)
		# print(pi.bb_serial_read_close(RX))
   	pi.bb_serial_read_open(RX, 9600, 8)
		time.sleep(0.1)	
		print "DATA:"
		try:
				while 1:
				(count, data) = pi.bb_serial_read(RX)
				print count
        		if count:
								data_hex = bytes2hex(data)
								print("data hex",data_hex)
								check_data = check(data_hex)	
								print("check data",check_data)
								pmdata = data_read(check_data)
								print(pmdata) 
								data_upload(pmdata)	
								time.sleep(0.5)
		except KeyboardInterrupt:
    		print "close"
				pi.bb_serial_read_close(RX)
    		pi.stop()

if __name__ == "__main__":
    main()

