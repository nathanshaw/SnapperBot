###################################################
# Code for controling the SnapperBot System using
# the Yahoo Weather API
#
# Coded for the Installation "Digital Rain"
#
# By Nathan Villicana-Shaw
# CalArts MTIID
#
###################################################
import pywapi
import string
from os import system
import serial, time
import random

#################################################
#            Variables to Change
#################################################

#are three or four arrays attached to each SnapperBot
ARRAY_NUM = 4
#What is the number of bots you are using? (minus 1)
SNAPPERBOT_NUM = 2
#What port name is you arduino?
snapperBot = serial.Serial('/dev/tty.usbmodem1d11111', 9600, timeout = 0.1)
#
##-------------------------------------------------
##           SnapperBot Command Functions
##-------------------------------------------------
#
time.sleep(6)
#
def writeSerial(botNum, messageByte):
    flag = chr(255)
    botChar = chr(botNum)
    msgChar = chr(messageByte)
    msgString = (flag, botChar, msgChar)
    snapperBot.write(msgString)
    print(msgString)

def singleSwitch(botNum, bankNum, switchNum):
    msgByte = (bankNum << 4)
    msgByte = (switchNum << 1) | msgByte
    writeSerial(botNum, msgByte)
    print("singleSwitch : ", botNum, ',', bankNum,',' , switchNum)

def multiSwitch(botNum, bankNum, velocity):
    msgByte = (bankNum << 4) | 64
    msgByte = (velocity << 1) | msgByte
    writeSerial(botNum, msgByte)
    print("multiSwitch : ", botNum, bankNum , velocity)


#-------------------------------------------------
#              Weather API Stuff
#-------------------------------------------------

noaa_station_names = ['VWS', 'PFAL', 'KJFK', 'PAMR', 'KEET', 'ASPA', 'TT127', 'MABL', 'MACR', 'CCSL', 'KAJO', 'KPSP', 'RFN', 'KRCV', 'SA00', 'KSNC', 'KIJL', 'AN120', 'D1189', 'NA2', 'BRTW',  'BALM', 'PGUM', '52200', 'PHHN', 'AR427', 'KFEP', 'SG04', 'KCBK','KFSK', 'LSUA', 'KAUD', 'k01T', '1LSU', 'KCHI', 'PHII', 'KOK1', 'K8A0', 'KHKA', 'KBYH', 'KCMD', 'KVOA', 'K4C0', 'KQT8', 'KQT9','KP92', 'EPO', 'BARH', 'BRU5', 'KBXM', 'UNIV', 'SOWR', 'SUP1', 'LANS', 'K96D', 'KBAC', 'BLDN8', 'AFRP4', 'MOCP4', 'YABP4', 'LTBV3', 'D8627', '41051']

noaa_result = pywapi.get_weather_from_noaa('KJFK')


#-------------------------------------------------
#                 Say Functions
#-------------------------------------------------
def sayNOAA():
    system('say ' +  "NOAA says: It is " + str(weather) + " and " + str(temp_f) + "Fahrenheit  now in" + location  + "&\n" )

#-------------------------------------------------
#                   Main Loop
#-------------------------------------------------

temp_f = 70
weather = 'sunny'
windchill_f =  12
sugested_pickup_period = 24
suggested_pickup = 30
dewpoint_f = 60
location = 'location'
wind_mpf = 23
#wind_dir =
wind_degrees = 280
pressure_in = 'pressure_in'
longitude = 240
latitude = 300
relative_humidity = 80

while True:
    random_station_name = noaa_station_names[random.randint(0, len(noaa_station_names) - 1)]
    noaa_result = pywapi.get_weather_from_noaa(random_station_name)
    #if (len(noaa_result) > 30):
     if 'temp_f' in  noaa_result:

        ##noaa_values = noaa_result.values()
        #print(type(noaa_result))
        #print(noaa_result.values())
        #print(noaa_result.keys())
        ##Temp
        temp_f = noaa_result['temp_f']
        ##overcast, sunny, etc
        ##weather = noaa_result['weather']
        #windchill_f = noaa_result['windchill_f']
        ##not sure what these are but they vary from station to station
        #sugested_pickup_period = noaa_result['sugested_pickup_period']
        #suggested_pickup = noaa_result['sugested_pickup']
        ##dewpoint
        ##dewpoint_f = noaa_result['dewpoint_f']
        ##string of the name and state or terratory
        ##location = noaa_result['location']
        ##wind stuff
        #wind_mpf = noaa_result['wind_mpf']
        ##wind_dir = noaa_result['wind_dir']
        ##wind_degrees = noaa_result['wind_degrees']
        ##pressure
        ##pressure_in = noaa_result['pressure_in']
        ##location
        ###location = noaa_result['location']
        ###longitude = noaa_result['longitude']
        ###latitude = noaa_result['latitude']
        ##humidity
        ###relative_humidity = noaa_result['relative_humidity']
        print(noaa_values)
        print(len(noaa_values))
        sayNOAA()
        #weatherString = noaa_values.encode("ascii")
        #print(type(weatherString))
        #print(weatherString)
        #weatherInts = [ord(weatherChar) for weatherChar in weatherString]
        #print(type(weatherInts))
        #print(weatherInts)
        #time.sleep(8)
    """
    for i in range(temp_f):
        for i in range(len(weatherInts) - 1):
            print(weatherInts[i]),
            writeSerial(random.randint(0, SNAPPERBOT_NUM), weatherInts[i])
            multiSwitch(random.randint(0,1), random.randint(0,3), weatherInts[i])
            time.sleep(temp_f * random.randfloat(0.0038,0.0042))

            """
