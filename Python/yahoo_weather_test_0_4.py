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
from threading import Thread

#################################################
#            Variables to Change
#################################################

#are three or four arrays attached to each SnapperBot
ARRAY_NUM = 4
#What is the number of bots you are using? (minus 1)
SNAPPERBOT_NUM = 2
#What port name is you arduino?
snapperBot = serial.Serial('/dev/tty.usbmodem1d11411', 57600, timeout = 0.1)
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
    #print(msgString)

def clearSnappers():
        msgString = (0xff,0xff,0xff)
        snapperBot.write(msgString)


def singleSwitch(botNum, bankNum, switchNum):
    msgByte = (bankNum << 4)
    msgByte = (switchNum << 1) | msgByte
    writeSerial(botNum, msgByte)
    #print("singleSwitch : ", botNum, ',', bankNum,',' , switchNum)

def multiSwitch(botNum, bankNum, velocity):
    msgByte = (bankNum << 4) | 64
    msgByte = (velocity << 1) | msgByte
    writeSerial(botNum, msgByte)
    #print("multiSwitch : ", botNum, bankNum , velocity)

def arraySwipe(data, delay):
    for i in range (int(data)):
        singleSwitch(i%6, i%4, i%8)
        time.sleep(delay)

def arrayBlast(data):
    for i in range (data):
        multiSwitch(i%6, i%4, i%8)
        time.sleep(.15)

def rain(botNum,bankNum,switchNum):
    while True:
        singleSwitch(botNum,bankNum,switchNum);
        rand1 = random.uniform(.5,4)
        time.sleep(rand1);

def nathanRain(speed):
    for i in range (100):
        multiSwitch(random.randint(0,5), random.randint(0,3), random.randint(0,7))
        time.sleep(speed/random.randint(1500,3000))

def testRain():
    for i in range(0,1000):
        rand0 = random.randint(0,6)
        rand1 = random.uniform(.01,.2)
        rand2 = random.randint(0,5)
        rand3 = random.randint(0,3)
        rand4 = random.randint(0,7)
        if rand0 < 5 :
            singleSwitch(rand2,rand3,rand4)
            time.sleep(rand1)
        else:
            multiSwitch(rand2,rand3,rand4)

#def arrayBlast1(data):
#   for i in range (data):
#      multiSwitch(0, i%4, 7)
#     multiSwitch(1, i%4, 7)
#    time.sleep(.15)

def bankSweep(data, time1): #cool one
    for i in range (data):
        multiSwitch(0,0,i%8)
        multiSwitch(0,1,i%8)
        multiSwitch(0,2,i%8)
        multiSwitch(0,3,i%8)
        multiSwitch(1,0,i%8)
        multiSwitch(1,1,i%8)
        multiSwitch(1,2,i%8)
        multiSwitch(1,3,i%8)
        multiSwitch(2,0,i%8)
        multiSwitch(2,1,i%8)
        multiSwitch(2,2,i%8)
        multiSwitch(2,3,i%8)
        multiSwitch(3,0,i%8)
        multiSwitch(3,1,i%8)
        multiSwitch(3,2,i%8)
        multiSwitch(3,3,i%8)
        multiSwitch(4,0,i%8)
        multiSwitch(4,1,i%8)
        multiSwitch(4,2,i%8)
        multiSwitch(4,3,i%8)
        multiSwitch(5,0,i%8)
        multiSwitch(5,1,i%8)
        multiSwitch(5,2,i%8)
        multiSwitch(5,3,i%8)

        time.sleep(time1)

def functionbleh(time1, time2, data):
    for i in range (int(data)):
        multiSwitch(0,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(5,i%4,i%8)
        time.sleep(time1)
        multiSwitch(0,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(5,i%4,i%8)
        time.sleep(time2)

def sunny(temp):
    testRain();

def overcast(temp):
    for i in range(20,100):
        bankSweep(4,i*(0.00001*temp))

def clear(temp_f):
    functionbleh(.00001*temp_f,.00015*temp_f,30)
    functionbleh(.000009*temp_f,.00012*temp_f,30)
    functionbleh(.000009*temp_f,.00075*temp_f,100)
    functionbleh(.000008*temp_f,.00055*temp_f,100)
    functionbleh(.000007*temp_f,.00015*temp_f,100)
    functionbleh(.000006*temp_f,.00025*temp_f,100)

def partlyCloudy(temp):
    for i in range(0,40):
        if (i%10 == 0):
            arraySwipe(temp*random.uniform(1,4), random.uniform(0.0000009, 0.0000012)*temp)
            time.sleep(temp/random.randint(100,200))
        else:
                functionbleh(random.uniform(0.0000006, 0.0000009*temp), random.uniform(0.0000004, 0.000099*temp), temp)

def aFewClouds(temp):
    functionbleh(0.0005*temp, 0.0001*temp, temp)
    functionbleh(0.00089*temp, 0.0004*temp, temp)
    functionbleh(0.00009*temp, 0.00008*temp, temp)



def fair(temp):
    nathanRain(temp*4);

def mostlyCloudy(temp):

    functionbleh(.00002*temp,.002,10)
    functionbleh(.00001*temp,.001,10)
    functionbleh(.000015*temp,.0015,10)
    functionbleh(.000015*temp,.0013,10)
    functionbleh(.00015*temp,.001,10)
    functionbleh(.000018*temp,.001,10)
    functionbleh(.00002*temp,.0011,100)
    functionbleh(.000024*temp,.0015,100)
    functionbleh(.00003*temp,.002,10)
    functionbleh(.00001*temp,.002,100)
    functionbleh(.00009*temp,.005,100)
    functionbleh(.00001*temp,.002,50)
    functionbleh(.00016*temp,.0014,100)
    functionbleh(.00002*temp,.0011,10)
    functionbleh(.00019*temp,.0017,50)
    functionbleh(.00002*temp,.0011,10)
    functionbleh(.000028*temp,.0015,10)
    functionbleh(.00006*temp,.008,100)
    functionbleh(.00004*temp,.006,75)
    functionbleh(.000009*temp,.0055,10)
    functionbleh(.000008*temp,.0055,10)
    functionbleh(.000007*temp,.0055,10)
    functionbleh(.000006*temp,.0055,10)

#-------------------------------------------------
#              Weather API Stuff
#-------------------------------------------------

noaa_station_names = ['VWS', 'PFAL', 'KJFK', 'PAMR', 'KEET', 'ASPA', 'TT127', 'MABL', 'MACR', 'CCSL', 'KAJO', 'KPSP', 'RFN', 'KRCV', 'SA00', 'KSNC', 'KIJL', 'AN120', 'D1189', 'NA2', 'BRTW',  'BALM', 'PGUM', '52200', 'PHHN', 'AR427', 'KFEP', 'SG04', 'KCBK','KFSK', 'LSUA', 'KAUD', 'k01T', '1LSU', 'KCHI', 'PHII', 'KOK1', 'K8A0', 'KHKA', 'KBYH', 'KCMD', 'KVOA', 'K4C0', 'KQT8', 'KQT9','KP92', 'EPO', 'BARH', 'BRU5', 'KBXM', 'UNIV', 'SOWR', 'SUP1', 'LANS', 'K96D', 'KBAC',
'BLDN8', 'AFRP4', 'MOCP4', 'YABP4', 'LTBV3', 'D8627', '41051', '91S', 'KZSE', 'K91S', 'CHAW', 'KCLS', 'AGKO', 'BATO', 'BANO', 'BEWO', 'K1B5', 'KOLD', 'K96B','MRSNV']

noaa_result = pywapi.get_weather_from_noaa('KJFK')


#-------------------------------------------------
#                 Say Functions
#-------------------------------------------------
def sayNOAA():
    system('say ' +  "It is " + str(weather) + " and " + str(temp_f) + " Fahrenheit  now in" + location  + " ,And the wind blows " + str(wind_dir) + "&\n" )

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
    noaa_values = noaa_result.values()
    noaa_keys = noaa_result.keys()
    #print(noaa_keys)
    print("Printing the Values : ", noaa_values)
    if len(noaa_values) == 1:
        sayNOAA()
        fair(2)
        #time.sleep(5);

    elif 'temp_f' and 'weather' and 'location' and 'wind_degrees' and 'wind_mpf' and 'wind_dir'  in  noaa_result:


        location = noaa_result['location']
        #print("Location is :", location)
        ##wind stuff
        #wind_mph = noaa_result['wind_mph']
        #print("wind_mpf : ", wind_mph)
        wind_dir = noaa_result['wind_dir']
        #print("wind_dir : ", wind_dir)
        #wind_degrees = noaa_result['wind_degrees']
        #print("wind_degrees are : ", wind_degrees)
        #print(type(noaa_result))
        #print(noaa_result.values())
        #print(noaa_result.keys())
        ##Temp
        if 'temp_f' in noaa_result:
            temp_f = float(noaa_result['temp_f'])
        #print("Temperature in F is :", temp_f)
        ##overcast, sunny, etc

        if 'weather' in noaa_result:
            weather = noaa_result['weather']
            #sayNOAA()
            #time.sleep(5)
            if weather == 'Mostly Cloudy':
                print("Mostly Cloudy Match")
                mostlyCloudy(temp_f)
                mostlyCloudy(temp_f)
                clearSnappers()
            elif weather == 'Partly Cloudy':
                print("Partly Cloudy Match")
                clearSnappers()
                partlyCloudy(temp_f)
                partlyCloudy(temp_f)
                clearSnappers()
            elif weather == 'Clear':
                print("Clear Match");
                clearSnappers()
                clear(temp_f)
                clear(temp_f)
                clearSnappers()
            elif weather == 'Overcast':
                print("Overcast Match")
                clearSnappers()
                overcast(temp_f)
                overcast(temp_f)
                clearSnappers()
            elif weather == 'Fair':
                clearSnappers()
                print("Fair Match")
                fair(temp_f)
                fair(temp_f)
                clearSnappers()
            elif weather == 'A Few Clouds':
                print("A Few Clouds Match")
                clearSnappers()
                aFewClouds(temp_f)
                aFewClouds(temp_f)
                clearSnappers()
            else :
                clearSnappers()
                #noMatch(temp_f)
                print("No Match")

        sayNOAA()
        time.sleep(1)
        fair(2)
        time.sleep(1)
        fair(2)
        time.sleep(1)
        fair(2)
        time.sleep(1)
        fair(2)
        time.sleep(1)
        fair(2)
        #windchill_f = noaa_result['windchill_f']
        ##not sure what these are but they vary from station to station
        #sugested_pickup_period = noaa_result['sugested_pickup_period']
        #suggested_pickup = noaa_result['sugested_pickup']
        ##dewpoint
        ##dewpoint_f = noaa_result['dewpoint_f']
        ##string of the name and state or terratory
        ##pressure
        ##pressure_in = noaa_result['pressure_in']
        ##location
        ###location = noaa_result['location']
        ###longitude = noaa_result['longitude']
        ###latitude = noaa_result['latitude']
        ##humidity
        ###relative_humidity = noaa_result['relative_humidity']
        #print(len(noaa_values))
        #weatherString = noaa_values.encode("ascii")
        #print(type(weatherString))
        #print(weatherString)
        #weatherInts = [ord(weatherChar) for weatherChar in weatherString]
        #print(type(weatherInts))
        #print(weatherInts)
        #time.sleep(8)

    else:
        time.sleep(1)

    """
    for i in range(temp_f):
        for i in range(len(weatherInts) - 1):
            print(weatherInts[i]),
            writeSerial(random.randint(0, SNAPPERBOT_NUM), weatherInts[i])
            multiSwitch(random.randint(0,1), random.randint(0,3), weatherInts[i])
            time.sleep(temp_f * random.randfloat(0.0038,0.0042))

            """

def Main():


    t1 = Thread(target=rain, args=(1,0,0))
    t2 = Thread(target=rain, args=(1,0,1))
    t3 = Thread(target=rain, args=(1,0,2))
    t4 = Thread(target=rain, args=(1,0,3))
    t5 = Thread(target=rain, args=(1,0,4))
    t6 = Thread(target=rain, args=(1,0,5))
    t7 = Thread(target=rain, args=(1,0,6))
    t8 = Thread(target=rain, args=(1,0,7))
    t9 = Thread(target=rain, args=(1,1,0))
    t10 = Thread(target=rain, args=(1,1,1))
    t11 = Thread(target=rain, args=(1,1,2))
    t12 = Thread(target=rain, args=(1,1,3))
    t13 = Thread(target=rain, args=(1,1,4))
    t14 = Thread(target=rain, args=(1,1,5))
    t15 = Thread(target=rain, args=(1,1,6))
    t16 = Thread(target=rain, args=(1,1,7))
    t17 = Thread(target=rain, args=(1,2,0))
    t18 = Thread(target=rain, args=(1,2,1))
    t19 = Thread(target=rain, args=(1,2,2))
    t20 = Thread(target=rain, args=(1,2,3))
    t21 = Thread(target=rain, args=(1,2,4))
    t22 = Thread(target=rain, args=(1,2,5))
    t23 = Thread(target=rain, args=(1,2,6))
    t24 = Thread(target=rain, args=(1,2,7))
    t25 = Thread(target=rain, args=(1,3,0))
    t26 = Thread(target=rain, args=(1,3,1))
    t27 = Thread(target=rain, args=(1,3,2))
    t28 = Thread(target=rain, args=(1,3,3))
    t29 = Thread(target=rain, args=(1,3,4))
    t30 = Thread(target=rain, args=(1,3,5))
    t31 = Thread(target=rain, args=(1,3,6))
    t32 = Thread(target=rain, args=(1,3,7))
    t33 = Thread(target=rain, args=(0,0,0))
    t34 = Thread(target=rain, args=(0,0,1))
    t35 = Thread(target=rain, args=(0,0,2))
    t36 = Thread(target=rain, args=(0,0,3))
    t37 = Thread(target=rain, args=(0,0,4))
    t38 = Thread(target=rain, args=(0,0,5))
    t39 = Thread(target=rain, args=(0,0,6))
    t40 = Thread(target=rain, args=(0,0,7))
    t41 = Thread(target=rain, args=(0,1,0))
    t42 = Thread(target=rain, args=(0,1,1))
    t43 = Thread(target=rain, args=(0,1,2))
    t44 = Thread(target=rain, args=(0,1,3))
    t45 = Thread(target=rain, args=(0,1,4))
    t46 = Thread(target=rain, args=(0,1,5))
    t47 = Thread(target=rain, args=(0,1,6))
    t48 = Thread(target=rain, args=(0,1,7))
    t49 = Thread(target=rain, args=(0,2,0))
    t50 = Thread(target=rain, args=(0,2,1))
    t51 = Thread(target=rain, args=(0,2,2))
    t52 = Thread(target=rain, args=(0,2,3))
    t53 = Thread(target=rain, args=(0,2,4))
    t54 = Thread(target=rain, args=(0,2,5))
    t55 = Thread(target=rain, args=(0,2,6))
    t56 = Thread(target=rain, args=(0,2,7))
    t57 = Thread(target=rain, args=(0,3,0))
    t58 = Thread(target=rain, args=(0,3,1))
    t59 = Thread(target=rain, args=(0,3,2))
    t60 = Thread(target=rain, args=(0,3,3))
    t61 = Thread(target=rain, args=(0,3,4))
    t62 = Thread(target=rain, args=(0,3,5))
    t63 = Thread(target=rain, args=(0,3,6))
    t64 = Thread(target=rain, args=(0,3,7))
    t65 = Thread(target=rain, args=(2,0,0))
    t66 = Thread(target=rain, args=(2,0,1))
    t67 = Thread(target=rain, args=(2,0,2))
    t68 = Thread(target=rain, args=(2,0,3))
    t69 = Thread(target=rain, args=(2,0,4))
    t70 = Thread(target=rain, args=(2,0,5))
    t71 = Thread(target=rain, args=(2,0,6))
    t72 = Thread(target=rain, args=(2,0,7))
    t73 = Thread(target=rain, args=(2,1,0))
    t74 = Thread(target=rain, args=(2,1,1))
    t75 = Thread(target=rain, args=(2,1,2))
    t76 = Thread(target=rain, args=(2,1,3))
    t77 = Thread(target=rain, args=(2,1,4))
    t78 = Thread(target=rain, args=(2,1,5))
    t79 = Thread(target=rain, args=(2,1,6))
    t80 = Thread(target=rain, args=(2,1,7))
    t81 = Thread(target=rain, args=(2,2,0))
    t82 = Thread(target=rain, args=(2,2,1))
    t83 = Thread(target=rain, args=(2,2,2))
    t84 = Thread(target=rain, args=(2,2,3))
    t85 = Thread(target=rain, args=(2,2,4))
    t86 = Thread(target=rain, args=(2,2,5))
    t87 = Thread(target=rain, args=(2,2,6))
    t88 = Thread(target=rain, args=(2,2,7))
    t89 = Thread(target=rain, args=(2,3,0))
    t90 = Thread(target=rain, args=(2,3,1))
    t91 = Thread(target=rain, args=(2,3,2))
    t92 = Thread(target=rain, args=(2,3,3))
    t93 = Thread(target=rain, args=(2,3,4))
    t94 = Thread(target=rain, args=(2,3,5))
    t95 = Thread(target=rain, args=(2,3,6))
    t96 = Thread(target=rain, args=(2,3,7))
    t97 = Thread(target=rain, args=(3,0,0))
    t98 = Thread(target=rain, args=(3,0,1))
    t99 = Thread(target=rain, args=(3,0,2))
    t100 = Thread(target=rain, args=(3,0,3))
    t101 = Thread(target=rain, args=(3,0,4))
    t102 = Thread(target=rain, args=(3,0,5))
    t103 = Thread(target=rain, args=(3,0,6))
    t104 = Thread(target=rain, args=(3,0,7))
    t105 = Thread(target=rain, args=(3,1,0))
    t106 = Thread(target=rain, args=(3,1,1))
    t107 = Thread(target=rain, args=(3,1,2))
    t108 = Thread(target=rain, args=(3,1,3))
    t109 = Thread(target=rain, args=(3,1,4))
    t110 = Thread(target=rain, args=(3,1,5))
    t111 = Thread(target=rain, args=(3,1,6))
    t112 = Thread(target=rain, args=(3,1,7))
    t113 = Thread(target=rain, args=(3,2,0))
    t114 = Thread(target=rain, args=(3,2,1))
    t115 = Thread(target=rain, args=(3,2,2))
    t116 = Thread(target=rain, args=(3,2,3))
    t117 = Thread(target=rain, args=(3,2,4))
    t118 = Thread(target=rain, args=(3,2,5))
    t119 = Thread(target=rain, args=(3,2,6))
    t120 = Thread(target=rain, args=(3,2,7))
    t121 = Thread(target=rain, args=(3,3,0))
    t122 = Thread(target=rain, args=(3,3,1))
    t123 = Thread(target=rain, args=(3,3,2))
    t124 = Thread(target=rain, args=(3,3,3))
    t125 = Thread(target=rain, args=(3,3,4))
    t126 = Thread(target=rain, args=(3,3,5))
    t127 = Thread(target=rain, args=(3,3,6))
    t128 = Thread(target=rain, args=(3,3,7))
    t129 = Thread(target=rain, args=(4,0,0))
    t130 = Thread(target=rain, args=(4,0,1))
    t131 = Thread(target=rain, args=(4,0,2))
    t132 = Thread(target=rain, args=(4,0,3))
    t133 = Thread(target=rain, args=(4,0,4))
    t134 = Thread(target=rain, args=(4,0,5))
    t135 = Thread(target=rain, args=(4,0,6))
    t136 = Thread(target=rain, args=(4,0,7))
    t137 = Thread(target=rain, args=(4,1,0))
    t138 = Thread(target=rain, args=(4,1,1))
    t139 = Thread(target=rain, args=(4,1,2))
    t140 = Thread(target=rain, args=(4,1,3))
    t141 = Thread(target=rain, args=(4,1,4))
    t142 = Thread(target=rain, args=(4,1,5))
    t143 = Thread(target=rain, args=(4,1,6))
    t144 = Thread(target=rain, args=(4,1,7))
    t145 = Thread(target=rain, args=(4,2,0))
    t146 = Thread(target=rain, args=(4,2,1))
    t147 = Thread(target=rain, args=(4,2,2))
    t148 = Thread(target=rain, args=(4,2,3))
    t149 = Thread(target=rain, args=(4,2,4))
    t150 = Thread(target=rain, args=(4,2,5))
    t151 = Thread(target=rain, args=(4,2,6))
    t152 = Thread(target=rain, args=(4,2,7))
    t153 = Thread(target=rain, args=(4,3,0))
    t154 = Thread(target=rain, args=(4,3,1))
    t155 = Thread(target=rain, args=(4,3,2))
    t156 = Thread(target=rain, args=(4,3,3))
    t157 = Thread(target=rain, args=(4,3,4))
    t158 = Thread(target=rain, args=(4,3,5))
    t159 = Thread(target=rain, args=(4,3,6))
    t160 = Thread(target=rain, args=(4,3,7))
    t161 = Thread(target=rain, args=(5,0,0))
    t162 = Thread(target=rain, args=(5,0,1))
    t163 = Thread(target=rain, args=(5,0,2))
    t164 = Thread(target=rain, args=(5,0,3))
    t165 = Thread(target=rain, args=(5,0,4))
    t166 = Thread(target=rain, args=(5,0,5))
    t167 = Thread(target=rain, args=(5,0,6))
    t168 = Thread(target=rain, args=(5,0,7))
    t169 = Thread(target=rain, args=(5,1,0))
    t170 = Thread(target=rain, args=(5,1,1))
    t171 = Thread(target=rain, args=(5,1,2))
    t172 = Thread(target=rain, args=(5,1,3))
    t173 = Thread(target=rain, args=(5,1,4))
    t174 = Thread(target=rain, args=(5,1,5))
    t175 = Thread(target=rain, args=(5,1,6))
    t176 = Thread(target=rain, args=(5,1,7))
    t177 = Thread(target=rain, args=(5,2,0))
    t178 = Thread(target=rain, args=(5,2,1))
    t179 = Thread(target=rain, args=(5,2,2))
    t180 = Thread(target=rain, args=(5,2,3))
    t181 = Thread(target=rain, args=(5,2,4))
    t182 = Thread(target=rain, args=(5,2,5))
    t183 = Thread(target=rain, args=(5,2,6))
    t184 = Thread(target=rain, args=(5,2,7))
    t185 = Thread(target=rain, args=(5,3,0))
    t186 = Thread(target=rain, args=(5,3,1))
    t187 = Thread(target=rain, args=(5,3,2))
    t188 = Thread(target=rain, args=(5,3,3))
    t189 = Thread(target=rain, args=(5,3,4))
    t190 = Thread(target=rain, args=(5,3,5))
    t191 = Thread(target=rain, args=(5,3,6))
    t192 = Thread(target=rain, args=(5,3,7))





    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()
    t20.start()
    t21.start()
    t22.start()
    t23.start()
    t24.start()
    t25.start()
    t26.start()
    t27.start()
    t28.start()
    t29.start()
    t30.start()
    t31.start()
    t32.start()
    t33.start()
    t34.start()
    t35.start()
    t36.start()
    t37.start()
    t38.start()
    t39.start()
    t40.start()
    t41.start()
    t42.start()
    t43.start()
    t44.start()
    t45.start()
    t46.start()
    t47.start()
    t48.start()
    t49.start()
    t50.start()
    t51.start()
    t52.start()
    t53.start()
    t54.start()
    t55.start()
    t56.start()
    t57.start()
    t58.start()
    t59.start()
    t60.start()
    t61.start()
    t62.start()
    t63.start()
    t64.start()
    t65.start()
    t67.start()
    t68.start()
    t69.start()
    t70.start()
    t71.start()
    t72.start()
    t73.start()
    t74.start()
    t75.start()
    t76.start()
    t77.start()
    t78.start()
    t79.start()
    t80.start()
    t81.start()
    t82.start()
    t83.start()
    t84.start()
    t85.start()
    t86.start()
    t87.start()
    t88.start()
    t89.start()
    t90.start()
    t91.start()
    t92.start()
    t93.start()
    t94.start()
    t95.start()
    t96.start()
    t97.start()
    t98.start()
    t99.start()
    t100.start()
    t101.start()
    t102.start()
    t103.start()
    t104.start()
    t105.start()
    t106.start()
    t107.start()
    t108.start()
    t109.start()
    t110.start()
    t111.start()
    t112.start()
    t113.start()
    t114.start()
    t115.start()
    t116.start()
    t117.start()
    t118.start()
    t119.start()
    t120.start()
    t121.start()
    t122.start()
    t123.start()
    t124.start()
    t125.start()
    t126.start()
    t127.start()
    t128.start()
    t129.start()
    t130.start()
    t131.start()
    t132.start()
    t132.start()
    t133.start()
    t134.start()
    t135.start()
    t136.start()
    t137.start()
    t138.start()
    t139.start()
    t140.start()
    t141.start()
    t142.start()
    t143.start()
    t144.start()
    t145.start()
    t146.start()
    t147.start()
    t148.start()
    t149.start()
    t150.start()
    t151.start()
    t152.start()
    t153.start()
    t154.start()
    t155.start()
    t156.start()
    t157.start()
    t158.start()
    t159.start()
    t160.start()
    t161.start()
    t162.start()
    t163.start()
    t164.start()
    t165.start()
    t166.start()
    t167.start()
    t168.start()
    t169.start()
    t170.start()
    t171.start()
    t172.start()
    t173.start()
    t174.start()
    t175.start()
    t176.start()
    t177.start()
    t178.start()
    t179.start()
    t180.start()
    t181.start()
    t182.start()
    t183.start()
    t184.start()
    t185.start()
    t186.start()
    t187.start()
    t188.start()
    t189.start()
    t190.start()
    t191.start()
    t192.start()
"""
    def Main():

    t1 = Thread(target=rain, args=(1,0,0))
    t2 = Thread(target=rain, args=(1,1,0))
    t3 = Thread(target=rain, args=(1,2,0))
    t4 = Thread(target=rain, args=(1,3,0))
    t5 = Thread(target=rain, args=(2,0,0))
    t6 = Thread(target=rain, args=(2,1,0))
    t7 = Thread(target=rain, args=(2,2,0))
    t8 = Thread(target=rain, args=(2,3,0))
    t9 = Thread(target=rain, args=(3,0,0))
    t10 = Thread(target=rain, args=(3,1,0))
    t11 = Thread(target=rain, args=(3,2,0))
    t12 = Thread(target=rain, args=(3,3,0))
    t13 = Thread(target=rain, args=(4,0,0))
    t14 = Thread(target=rain, args=(4,1,0))
    t15 = Thread(target=rain, args=(4,2,0))
    t16 = Thread(target=rain, args=(4,3,0))
    t17 = Thread(target=rain, args=(5,0,0))
    t18 = Thread(target=rain, args=(5,1,0))
    t19 = Thread(target=rain, args=(5,2,0))
    t20 = Thread(target=rain, args=(5,3,0))
    t21 = Thread(target=rain, args=(0,0,0))
    t22 = Thread(target=rain, args=(0,1,0))
    t23 = Thread(target=rain, args=(0,2,0))
    t24 = Thread(target=rain, args=(0,3,0))


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()
    t20.start()
    t21.start()
    t22.start()
    t23.start()
    t24.start()


"""



