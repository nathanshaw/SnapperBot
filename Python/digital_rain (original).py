###################################################
# Code for controling the SnapperBot System using
# the Yahoo Weather API
#
# Coded for the Installation "Digital Rain"
#
# By Nathan Villicana-Shaw with help from Jake Penn
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


temp_f = 90
weather = 'sunny'
location = 'Santa Clarita'
locationi = 'Santa Clarita'
wind_speed = 7
wind_dir = 'west'
#are three or four arrays attached to each SnapperBot
ARRAY_NUM = 4
#What is the number of bots you are using? (minus 1)
SNAPPERBOT_NUM = 5
#What port name is you arduino?
snapperBot = serial.Serial('/dev/tty.usbmodem1d11411', 57600, timeout = 0.1)
#
##-------------------------------------------------
##           SnapperBot Command Functions (low Level)
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

def clearSnappers():
    msgString = (0xff,0xff,0xff)
    snapperBot.write(msgString)

def singleSwitch(botNum, bankNum, switchNum):
    msgByte = (bankNum << 4)
    msgByte = (switchNum << 1) | msgByte
    writeSerial(botNum, msgByte)

def multiSwitch(botNum, bankNum, velocity):
    msgByte = (bankNum << 4) | 64
    msgByte = (velocity << 1) | msgByte
    writeSerial(botNum, msgByte)

def arraySwipe(data, delay):
    for i in range (int(data)):
        singleSwitch(i%6, i%4, i%8)
        time.sleep(delay)

def arrayBlast(data, _time):
    for i in range (data):
        multiSwitch(i%6, i%4, i%8)
        time.sleep(_time)

#
##-------------------------------------------------
##           Musical Functions (mid Level)
##-------------------------------------------------
#

def rain(botNum,bankNum,switchNum):
    while True:
        singleSwitch(botNum,bankNum,switchNum);
        rand1 = random.uniform(.0005,0.004)
        time.sleep(rand1);

def nathanRain(speed, wind, chance, range1):
    for i in range (range1):
        factor = chance * random.uniform(0,1)
        if factor > 0.5:
            multiSwitch(random.randint(0,5), random.randint(0,3), random.randint(0,7))
        else :
            singleSwitch(random.randint(0,5), random.randint(0,3), random.randint(0,7))
        time.sleep(speed/random.uniform(150*wind,300*wind))

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

def nathanBeat(number1, number2, temp):
    for i in range(int(temp)):

        multiSwitch(0,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(5,i%4,i%8)
        time.sleep(number1)
        multiSwitch(1,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(5,i%4,i%8)
        time.sleep(number2/2)
        multiSwitch(1,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(5,i%4,i%8)
        time.sleep(number1/2)
        multiSwitch(0,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        time.sleep(number2*2)


def nathanAllFreak(number1, number2, number3, _time):
    for i in range(int(number1)):
        nathanBankFreak(number2,number3,random.randint(0,5))
        time.sleep(_time)

def nathanBankFreak(number1,number2, arduino):
    for i in range (number1):
        for ii in range (number2):
            singleSwitch(arduino,ii%4,ii%8)
            time.sleep(0.00001)

def bankSweep(number, time1): #cool one

    for i in range (number):
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

def bankSweep1(number, time1): #cool one

    for i in range (number):
        multiSwitch(random.randint(0,5),random.randint(0,3),random.randint(0,7))
        singleSwitch(random.randint(0,5),random.randint(0,3),random.randint(0,7))
        singleSwitch(random.randint(0,5),random.randint(0,3),random.randint(0,7))
        singleSwitch(random.randint(0,5),random.randint(0,3),random.randint(0,7))
        singleSwitch(random.randint(0,5),random.randint(0,3),random.randint(0,7))
        time.sleep(time1)

def functionbleh1(time1, time2, data):

    for i in range (int(data)):
        multiSwitch(0,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        time.sleep((time1+time2)*0.34)
        multiSwitch(5,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        time.sleep(time2*0.77)
        multiSwitch(5,i%4,i%8)
        multiSwitch(3,i%4,i%8)
        multiSwitch(2,i%4,i%8)
        multiSwitch(1,i%4,i%8)
        multiSwitch(4,i%4,i%8)
        time.sleep(time2*0.77)

def functionbleh2(time1, time2, data):

    for i in range (int(data)):
        multiSwitch(0,i%4,i%3)
        singleSwitch(1,i%2,i%4)
        singleSwitch(2,i%4,i%2)
        multiSwitch(3,i%3,i%7)
        singleSwitch(4,i%4,i%8)
        multiSwitch(5,i%1,i%4)
        time.sleep(time1 * random.uniform(0.74,1.25))
        singleSwitch(0,i%4,i%8)
        multiSwitch(1,i%3,i%5)
        singleSwitch(2,i%4,i%6)
        multiSwitch(3,i%2,i%7)
        singleSwitch(4,i%3,i%2)
        multiSwitch(5,i%2,i%3)
        time.sleep(time2 * random.uniform(0.75, 1.25))

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
#
##-------------------------------------------------
##        Weather Functions (high level)
##-------------------------------------------------
#

def sunny(temp):

    for i in range(temp):
        nathanRain(temp*random.randint(0.2,0.5))

def partlyCloudy(temp, wind):
    wind = float(wind)
    wind = 2.5 + wind

    if temp < 20:
        temp = 19

    nathanAllFreak(int(temp/12),int(temp/20),50,random.uniform(0.001,0.003))
    functionbleh2(0.0024*wind, 0.0007*temp, int(temp*0.4))
    nathanRain(temp, wind*7, random.uniform(0.1,0.6), int(wind * 7));
    functionbleh2(0.0053*wind, 0.0012*temp, int(temp*0.6))
    nathanRain(temp, wind*2, random.uniform(0.1,0.4), int(wind * 7));
    nathanAllFreak(int(temp/7),int(temp/15),50,random.uniform(0.0006,0.002))
    nathanRain(temp, wind, random.uniform(0.2,0.6), int(wind * 7));
    functionbleh2(0.0045*temp, 0.0005*wind, int(wind*1.5))
    nathanRain(temp, wind*4, random.uniform(0.1,0.4), int(wind * 7));
    functionbleh2(0.0074*wind, 0.0008*wind, int((wind+temp)/2))
    nathanAllFreak(int(temp/17),int(temp/24),50,random.uniform(0.0001,0.001))

def overcast(temp_f, wind_s):

    wind_s = float(wind_s)
    temp_f = float(temp_f)

    for i in range (30,70):

        if i%int(wind_s) == 0:
            time.sleep(random.uniform(0.0075,0.02)*float(wind_s))

        if i%int(wind_s) == 13:
            time.sleep(random.uniform(0.0095,0.03)*float(wind_s))

        functionbleh(.00001*float(wind_s*5),.0000015*temp_f,int(i*.30))
        functionbleh(.000009*float(wind_s*5),.0000012*temp_f,int(i*0.35))

        if i%int(wind_s) == 16:
            time.sleep(random.uniform(0.0075,0.02)*float(wind_s))

        functionbleh(.000009*float(wind_s*5),.0000075*temp_f,int(i*0.1))
        functionbleh(.000008*float(wind_s*5),.0000155*temp_f,random.randint(1,5))
        time.sleep(random.uniform(0.005,0.005)*float(wind_s))
        functionbleh(.000007*float(wind_s*5),.0000015*temp_f,int(0.1*i))

        if i%int(wind_s) == 7:
            time.sleep(random.uniform(0.0075,0.02)*float(wind_s))

        functionbleh(.000006*float(wind_s*5),.0000125*float(temp_f),int(0.12*i))

def mostlyCloudy(temp, wind):

    wind = float(wind)

    for i in range(0,100):

        if (i%int(wind) == 0):

            for i in range(0,int(wind*0.25)):
                arraySwipe(temp*random.uniform(1,4), random.uniform(0.0000009, 0.0000012)*temp)
                time.sleep(temp/random.randint(70,200))

        else:
                functionbleh(random.uniform(0.00000006, 0.0000002)*temp, random.uniform(0.00000004, 0.00002)*temp, int(temp/2))
    time.sleep(6)

def aFewClouds(temp, wind):
    wind = float(wind)
    wind = 2.5 + wind

    if temp < 20:
        temp = 19

    functionbleh(0.0015*wind, 0.0001*temp, 10)
    nathanAllFreak(int(temp/12),int(temp/20),50,random.uniform(0.001,0.003))
    functionbleh1(0.0024*wind, 0.0004*temp, int(temp*0.6))
    functionbleh1(0.0053*wind, 0.00008*temp, int(temp*0.6))
    nathanAllFreak(int(temp/7),int(temp/15),50,random.uniform(0.0006,0.002))
    time.sleep((50 - wind)*0.005)
    functionbleh1(0.00035*temp, 0.00005*wind, int(wind*1.5))
    functionbleh1(0.0034*wind, 0.0001*wind, int((wind+temp)/2))
    nathanAllFreak(int(temp/17),int(temp/24),50,random.uniform(0.0001,0.001))
    time.sleep((50 - wind)*0.005)
    functionbleh(0.00033*temp, 0.00008*temp, wind*2)

def fair(temp, wind):

    if temp < 20:
        temp = 20
    if temp < 90:
        temp1 = temp
    else :
        temp1 = temp * 0.5

    wind = float(wind)
    nathanBeat(0.00189*temp, 0.0003*(wind*5), int(temp1*0.8))
    nathanRain(temp, wind, 0.4,  16)
    nathanBeat(0.001*temp, 0.00012*(wind*5), int(temp1*0.4))
    nathanRain(temp, wind, 0.4,  12)
    nathanBeat(0.0009*temp, 0.0025*(wind*5), int(temp1*.8))
    nathanRain(temp, wind, 0.4,  17)
    nathanBeat(0.0029*temp, 0.00012*(wind*5), int(temp1*0.2))
    nathanRain(temp, wind, 0.4,  12)
    nathanBeat(0.00149*temp, 0.00015*(wind*5), int(temp1*.2))
    nathanRain(temp, wind, 0.4,  13)
    nathanBeat(0.0018*temp, 0.006*(wind*5), int(temp1*0.4))
    nathanRain(temp, wind, 0.4,  22)
    nathanBeat(0.00229*temp, 0.00020*(wind*5), int(temp1*.8))

def clear(temp, windSpeed):
    for i in range (0,4):
        print(i)
        bankSweep1(int(temp*random.uniform(1.25,2)),random.uniform(0.03,0.18))

def drizzle(temp, windSpeed):
    for i in range(0, 10):
        nathanRain(temp*6, windSpeed*20, random.uniform(0.1,1.6), int(temp));
        nathanRain(temp*8, windSpeed*16, random.uniform(0.1,0.4), int(windSpeed * 7));
        nathanRain(temp*6.2, windSpeed*20, random.uniform(0.1,1.6), int(temp + windSpeed));
        nathanRain(temp*8, windSpeed*14, random.uniform(0.1,0.4), int(windSpeed * 6));

def raining(temp, wind):
    for i in range(1,3):
        temp = temp * random.uniform(0.9,6)
        if temp > 500:
            temp = 500
        windSpeed = wind * random.uniform(0.9,6)
        print("New Temp : ", temp, " New wind : ", windSpeed)
        nathanRain(temp*6, windSpeed*20, random.uniform(0.1,1.6), int(temp*2));
        nathanRain(temp*8, windSpeed*16, random.uniform(0.1,0.4), int(windSpeed * 14));
        nathanRain(temp*6.2, windSpeed*20, random.uniform(0.1,1.6), int(temp*2 + windSpeed*2));
        nathanRain(temp*8, windSpeed*14, random.uniform(0.1,0.4), int(windSpeed * 12));

def thunderstorm(temp, wind):

    functionbleh(.00002*temp,.0002*wind,10)
    functionbleh(.00001*temp,.0001*wind,10)
    functionbleh(.000015*temp,.00015*wind,10)
    functionbleh(.000015*temp,.00013*wind,20)
    functionbleh(.00015*temp,.0001*wind,10)
    functionbleh(.000018*temp,.0001*wind,30)
    functionbleh(.00002*temp,.00011*wind,50)
    functionbleh(.000024*temp,.00015*wind,100)
    functionbleh(.00003*temp,.0002*wind,10)
    functionbleh(.00001*temp,.0002*wind,10)
    functionbleh(.00009*temp,.0005*wind,70)
    functionbleh(.00001*temp,.0002*wind,50)
    functionbleh(.00016*temp,.00014*wind,100)
    functionbleh(.00002*temp,.00011*wind,10)
    functionbleh(.00019*temp,.00017*wind,30)
    functionbleh(.00002*temp,.00011*wind,10)
    functionbleh(.000028*temp,.00015*wind,10)
    functionbleh(.00006*temp,.0008*wind,100)
    functionbleh(.00004*temp,.0006*wind,75)
    functionbleh(.000009*temp,.00055*wind,10)
    functionbleh(.000008*temp,.00055*wind,10)
    functionbleh(.000007*temp,.00055*wind,10)
    functionbleh(.000006*temp,.00055*wind,10)

#-------------------------------------------------
#              Weather API Stuff
#-------------------------------------------------

stateABR = ['AK','AL','AR','AS','AZ','CA','CO','CT','DE','DC','FM','FL','GA','GU','HI','IA','ID','IL','IN','KS','KY','LA','MH','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PW','PA','PR','RI','SC','SD','TN','TX','UT','VA','VI','VT','WA','WI','WV','WY']
print(len(stateABR))
statesNAME = ['Alaska','Alabama','Arkansas','American Samoa','Arizona','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Iowa','Idaho','Illinois','Indiana','Kansas','Kentucky','Lousiana','Marshall Islands','Massachusetts','Maryland','Maine','Michigan','Minnesota','Missouri','Mississippi','Montana','North Carolina','North Dakota','Nebraska','New Hampshire','New Jersey','New Mexico','Nevada','New York','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Virginia','Virgine Islands','Vermont','Washington','Wisconsin','West Virginia','Wyoming']
print(len(statesNAME))

noaa_station_names = ['VWS', 'PFAL', 'KJFK', 'PAMR', 'KEET', 'ASPA', 'TT127', 'MABL', 'MACR', 'CCSL', 'KAJO', 'KPSP', 'RFN', 'KRCV', 'SA00', 'SV', 'TO', 'BBY4', 'KAJO','KSNC', 'KIJL', 'AN120', 'D1189', 'NA2', 'BRTW',  'BALM', 'PGUM', '52200', 'PHHN', 'AR427', 'KFEP', 'SG04', 'KCBK','KFSK', 'LSUA', 'KAUD', 'k01T', '1LSU', 'KCHI', 'PHII', 'KOK1', 'K8A0', 'KHKA', 'KBYH', 'KCMD', 'KVOA', 'K4C0', 'KQT8', 'KQT9','KP92', 'EPO', 'BARH', 'BRU5', 'KBXM', 'UNIV',
'SOWR','SUP1','KABR','KBKX','K9V9', 'K0V1','KRCA', 'KHON','LANS','K96D','KBAC','NSTU','PPG01', 'TT126', '51181', 'LATP6', 'NSTP6', 'MTCP7','WWHP7', 'PWAK', 'DDDP7', 'C6666', 'KLBL', 'KIAB', 'KAAO', 'MAOP4', 'SLMP4', 'YAHP4','KBHX', 'K064', 'KMHV', 'KMHS','BLDN8', 'AFRP4', 'MOCP4', 'YABP4', 'LTBV3', 'D8627', '41051', '91S', 'KZSE', 'K91S', 'CHAW', 'KCLS', 'AGKO', 'BATO', 'BANO', 'BEWO', 'K1B5', 'KOLD', 'K96B','MRSNV','KIYA', 'KBAD', 'KAEX', '1LSU', 'KBKV', 'KBCT', 'KCGC', 'KDED',
'KX91', 'KN78', 'KACY','K54N', 'KLDJ', 'KMJX', 'A1193','PIKN4',
'KWST', 'KUUU', 'K2B4', 'KBID', 'KSFZ', 'KPJI', 'KPVD']

#-------------------------------------------------
#                 Say Functions
#-------------------------------------------------
def sayNOAA():

    chance = random.randint(0,3)
    if chance < 2:
        system('say ' +  "It is " + str(weather) + " and " + str(temp_f) + " Fahrenheit  now in " + locationi  + " , ... And the wind blows " + str(wind_dir) + " At " + str(wind_speed) + " Miles Per Hour " + "&\n" )
    elif chance == 3:
        system('say ' +  "In  " + str(locationi) + " it is " + str(weather) +  " ,... And the wind blows at" + str(wind_speed) + " Miles Per Hour " + str(wind_dir) + "&\n" )
    else :
        system('say ' +  "It is " + str(temp_f) + " Fahrenheit and " + str(weather) + " now in " + str(locationi)  + " ... the wind blows " + str(wind_dir) + " At " + str(wind_speed) + " Miles an Hour " + "&\n" )

#-------------------------------------------------
#                   Main Loop
#-------------------------------------------------

print("|||||||||||||||||||||||||||||||||||||||||||||||||")
print(noaa_station_names)
print("|||||||||||||||||||||||||||||||||||||||||||||||||")
noaa_result = pywapi.get_weather_from_noaa('KJFK')

while True:
    random_station_name = noaa_station_names[random.randint(0, len(noaa_station_names) - 1)]
    print("Station Name : ", random_station_name)
    noaa_result = pywapi.get_weather_from_noaa(random_station_name)
    noaa_values = noaa_result.values()
    noaa_keys = noaa_result.keys()
    if len(noaa_values) == 1:
        if random.randint(0,10) < 7:
            sayNOAA()
        nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
        time.sleep(random.uniform(0.01,0.2))
        nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
        time.sleep(random.uniform(0.01,0.2))
        nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
        time.sleep(random.uniform(0.001,0.1))
        nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
        time.sleep(random.uniform(0.01,0.1))
        print("------------------------------")

    elif 'temp_f' and 'weather' and 'location' and 'wind_degrees' and 'wind_mpf' and 'wind_dir'  in  noaa_result:

        if 'location' in noaa_result:
            location = noaa_result['location']
            for i in range (0, len(stateABR) -1):
                locationi = string.replace(location, stateABR[i], statesNAME[i])
                if len(locationi) > len(location):
                   break
            print(location)

        if 'wind_mph' in noaa_result:
            wind_speed = float(noaa_result['wind_mph'])
            if wind_speed < 3:
                wind_speed = 3
            print("wind_mph             :",wind_speed)
            wind_dir = noaa_result['wind_dir']

            if 'temp_f' in noaa_result:
                temp_f = float(noaa_result['temp_f'])
                if temp_f < 3:
                    temp_f = 2
                print("Temperature in F is  :", temp_f)

            if 'weather' in noaa_result:

                weather = noaa_result['weather']
                #weather = weather + ' and Fog'
                print(weather)
                if random.randint(0,100) == 1:
                    weather = 'Thunderstorm'
                    print("------------------------------")
                    print("|||||||||||||||||||||||||")
                    print("VETO TO THUNDERSTORM")
                    print("|||||||||||||||||||||||||")
                    print("------------------------------")
                #weather = 'Thunderstorm'
                #weather = 'Rain'
                #weather = 'Light Drizzle'
                #weather = 'Overcast'
                #weather = 'Mostly Cloudy'
                #weather = 'Partly Cloudy'
                #weather = 'A Few Clouds'
                #weather = 'Fair'
                #weather = 'Clear'
                #weather = 'Car'

                if 'Fog' in weather:
                    wind_speed = wind_speed*0.5
                    temp_f = temp_f * 2
                    print("------------------------------")
                    print("Fog detected, wind speed changed to : ", wind_speed, " temp changed to : ", temp_f)

                if 'Mist' in weather:
                    wind_speed = wind_speed * 1.05
                    temp_f = temp_f * 0.5
                    print("------------------------------")
                    print("Mist detected wind speed changed to : ", wind_speed, " Temp changed to : ", temp_f)

                if 'Breezy' in weather:
                    wind_speed = wind_speed * 1.5
                    temp_f = temp_f * 0.8
                    print("------------------------------")
                    print("Breeze detected wind speed changed to : ", wind_speed, " Temp changed to : ", temp_f)

                if 'Rain' in weather:
                    time.sleep(2)
                    sayNOAA()
                    time.sleep(1.5)
                    clearSnappers()
                    if 'Light' in weather:
                        temp_f = temp_f * 1.5
                        print("------------------------------")
                        print("Light Rain Match")
                        print("------------------------------")
                    elif 'Heavy' in weather:
                        print("------------------------------")
                        print("Heavy Rain Match")
                        print("------------------------------")
                        raining(temp_f * 0.5, wind_speed * 0.75)
                        raining(temp_f * 0.7, wind_speed * 0.5)
                    else :
                        print("------------------------------")
                        print("Rain Match")
                        print("------------------------------")
                        raining(temp_f, wind_speed)
                    clearSnappers()

                elif  weather[:13] == 'Light Drizzle':
                    time.sleep(2)
                    sayNOAA()
                    time.sleep(1.5)
                    clearSnappers()
                    print("------------------------------")
                    print("Drizzle Match")
                    print("------------------------------")
                    drizzle(temp_f, wind_speed)
                    clearSnappers()

                elif weather[:4] == 'Fair':
                    if(temp_f < 14):
                        temp_f = 14
                    chance = random.randint(0,4)
                    if(chance < 1):
                        time.sleep(2)
                        sayNOAA()
                        time.sleep(1.5)
                        clearSnappers()
                        print("------------------------------")
                        print("Fair Match")
                        print("------------------------------")
                        fair(temp_f, (wind_speed + 5))
                        clearSnappers()
                    else:
                        print("------------------------------")
                        print("rejecting Fair : too common")
                        print("------------------------------")


                elif weather[:13] == 'Mostly Cloudy':
                    time.sleep(2)
                    sayNOAA()
                    if temp_f < 10:
                        temp_f = 10
                    print("------------------------------")
                    print("Mostly Cloudy Match")
                    print("------------------------------")
                    mostlyCloudy(temp_f, wind_speed)
                    mostlyCloudy(int(temp_f*0.7), wind_speed)
                    time.sleep(3)
                    clearSnappers()

                elif weather[:13] == 'Partly Cloudy':
                    time.sleep(2)
                    sayNOAA()
                    print("------------------------------")
                    print("Partly Cloudy Match")
                    print("------------------------------")
                    clearSnappers()
                    partlyCloudy(int(temp_f)*1.2, wind_speed*0.8)
                    clearSnappers()

                elif weather[:5] == 'Clear':
                    time.sleep(2)
                    sayNOAA()
                    if wind_speed < 4:
                        wind_speed = 4
                    print("------------------------------")
                    print("Clear Match");
                    print("------------------------------")
                    clearSnappers()
                    clear(temp_f, wind_speed)
                    clearSnappers()

                elif weather[:8] == 'Overcast' or weather[:8] == 'Fog/Mist' or weather[:14] == 'Fair with Haze':
                    time.sleep(2)
                    sayNOAA()
                    print("------------------------------")
                    print("Overcast Match")
                    print("------------------------------")
                    clearSnappers()
                    overcast(temp_f*0.5, wind_speed)
                    if 'Breezy' not in weather:
                        time.sleep(3)
                    overcast(temp_f*0.25, wind_speed)
                    overcast(temp_f*0.75, wind_speed*2)
                    overcast(temp_f, wind_speed)
                    #time.sleep((temp_f*0.2) + (wind_speed*0.5))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    nathanAllFreak(random.randint(1,3),random.randint(1,3),random.randint(100,250),random.uniform(0.00006,0.001))
                    clearSnappers()


                elif weather[:12] == 'A Few Clouds':
                    time.sleep(2)
                    sayNOAA()
                    print("------------------------------")
                    print("A Few Clouds Match")
                    print("------------------------------")
                    clearSnappers()
                    aFewClouds(temp_f*0.5, wind_speed*1.5)
                    aFewClouds(temp_f*0.5, wind_speed*1.5)
                    aFewClouds(temp_f*2, wind_speed*0.5)
                    aFewClouds(temp_f*2, wind_speed*0.5)
                    aFewClouds(temp_f*0.5, wind_speed*1.5)
                    aFewClouds(temp_f*0.5, wind_speed*1.5)
                    clearSnappers()

                elif weather[:12] == 'Thunderstorm':
                    time.sleep(2)
                    sayNOAA()
                    print("------------------------------")
                    print("ThunderStorm Match")
                    print("------------------------------")
                    clearSnappers()
                    thunderstorm(temp_f*random.uniform(1,2), wind_speed)
                    thunderstorm(temp_f*random.uniform(.1,.7), wind_speed)
                    thunderstorm(temp_f*random.uniform(0.4,3), wind_speed)
                    thunderstorm(temp_f*random.uniform(0.01,2.4), wind_speed)
                    thunderstorm(temp_f*random.uniform(.1,.7), wind_speed)
                    thunderstorm(temp_f*random.uniform(0.4,3), wind_speed)
                    clearSnappers()
                else :
                    print("------------------------------")
                    print("Printing the Values : ", noaa_values)
                    print("------------------------------")
                    print("No Match")
                    print("------------------------------")
                    print("No Match")
                    print("------------------------------")
                    print("No Match")
                    print("------------------------------")
                    print("No Match")
                    print("------------------------------")
                    time.sleep(2)
                    sayNOAA()
                    clearSnappers()
                    thunderstorm(temp_f*random.uniform(0.1,2.4))
                    thunderstorm(temp_f*random.uniform(.4,.17))
                    thunderstorm(temp_f*random.uniform(0.2,1))
                    clearSnappers()
                    #noMatch(temp_f)

            sayNOAA()

    else:
        nathanAllFreak(4,4,150,random.uniform(0.00001,0.0003))
        time.sleep(1)
        nathanAllFreak(4,4,150,random.uniform(0.00001,0.0003))
        nathanAllFreak(4,4,150,random.uniform(0.00001,0.0003))
