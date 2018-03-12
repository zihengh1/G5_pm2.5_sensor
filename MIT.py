#!/usr/bin/python

import sys
import time
import difflib
import pigpio
import httplib
import urllib

def cmp(a,b):
    return (a > b) - (a < b)

def check(new_string):
    new_list = []
    for x in new_string:
        new_list.append(x)
        
    standard = ["4","d","4","2"]
    
    if cmp(new_list[0:4], standard) == -1:
        for x in range(4):
            new_list.insert(x, standard[x])
        return new_list
    else:
        return new_list
    
def bytes2hex(s):
    return "".join("{:02x}".format(c) for c in s)

def data_read(data_hex):
    # pm1_cf = int(data_hex[8] + data_hex[9] + data_hex[10] + data_hex[11],16)
    # pm25_cf = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15],16)
    # pm10_cf = int(data_hex[16] + data_hex[17] + data_hex[18] + data_hex[19],16)
    # pm1 = int(data_hex[20] + data_hex[21] + data_hex[22] + data_hex[23],16)
    # pm25 = int(data_hex[24] + data_hex[25] + data_hex[26] + data_hex[27],16)
    # pm10 = int(data_hex[28] + data_hex[29] + data_hex[30] + data_hex[31],16)
    pm = int(data_hex[12] + data_hex[13] + data_hex[14] + data_hex[15], 16)
    return [pm]

def data_upload(pmdata, num):
    # if num == 1:
    #     API_key = "YAFYMHZWAA33M2PG"
    # elif num == 2:
    #     API_key = "58Z53NO5ELXCMZGN"
    # elif num == 3:
    #     API_key = "RCJGLISA04VE1FXF"
    API_key = "7OPOX3AVUEW7SEBJ"
    print("API_key: ",API_key)    
    
    # params = urllib.urlencode({'field1': pmdata[3], 'field2': pmdata[4], 'field3': pmdata[5], 'key':API_key})
    if num == 1:
        params = urllib.urlencode({'field1': pmdata[0], 'key':API_key})
    elif num == 2:
				params = urllib.urlencode({'field2': pmdata[0], 'key':API_key})
    elif num == 3:
				params = urllib.urlencode({'field3': pmdata[0], 'key':API_key})
    elif num == 4:
				params = urllib.urlencode({'field4': pmdata[0], 'key':API_key})

    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    tconn = httplib.HTTPConnection("api.thingspeak.com:80")
    tconn.request("POST", "/update", params, headers)
    response = tconn.getresponse()
    data = response.read()
    tconn.close()
    time.sleep(0.5)

def fun(RX, num):

    pi = pigpio.pi()
    pi.set_mode(RX, pigpio.INPUT)
    # pi.bb_serial_read_close(RX)
    pi.bb_serial_read_open(RX, 9600, 8)
    time.sleep(0.5)
    
    print("DATA: ",num)
    for x in range(10):
        print("x:",x)
        (count, data) = pi.bb_serial_read(RX)
        if count:
            data_hex = bytes2hex(data)
            print("data_hex",data_hex)
            
            check_data = check(data_hex)
            print("check_data",check_data)
            
            pmdata = data_read(check_data)
            print("pmdata",pmdata)
            
            data_upload(pmdata,num)
        # time.sleep(0.5)
    print("close")
    pi.bb_serial_read_close(RX)
    pi.stop()

def main():
    # RX = [23, 17, 18]
    RX = [18, 17] 
    num = 1
    try:
        while 1:
            for rx in RX:
                fun(rx,num)
                num = num + 1
						time.sleep(60)
						num = 1

    except KeyboardInterrupt:
				print("close")
				pi.bb_serial_read_close(RX[-1])
				pi.stop()
	
if __name__ == "__main__":
    main()

