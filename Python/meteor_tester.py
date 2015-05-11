import serial, time, random, array
#imports for OSC
import OSC, threading
#Serial initalize
snapperBot = serial.Serial('/dev/tty.usbserial-AI02G4US', 9600, timeout = 0.1)

time.sleep(6)

def switch_handler(addr, tags, stuff, source):
    multiSwitch(stuff[0], stuff[1], stuff[2])
    #print(addr, stuff[0], stuff[1], stuff[2])

#this is for troubleshotting the OSC
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"

def randomTest():
    flag = random.randint(1,6)
    #get random numbers to send
    randomMsg = random.randint(1, 3)
    #convert them to chars
    msgFlag = chr(flag)
    msgChar = chr(randomMsg)
    #add the chars together to form a string
    msgString = (msgFlag, msgChar)
    print(msgString)
    #write string to serial port
    #snapperBot.write(msgString)
    snapperBot.write(msgString);
    #wait 200ms before repeating
    time.sleep(0.005)

def writeSerial(botNum, messageByte):
    flag = chr(255)
    botChar = chr(botNum)
    msgChar = chr(messageByte)
    msgString = (flag, botChar, msgChar)
    snapperBot.write(msgString)
    #snapperBot.write(botChar)
    #snapperBot.write(msgChar)
    print(msgString)

#-------------------------------------------------
#           SnapperBot Command Functions
#-------------------------------------------------

def singleSwitch(botNum, bankNum, switchNum):
    msgByte = (bankNum << 4)
    msgByte = (switchNum << 1) | msgByte
    writeSerial(botNum, msgByte)
    #print("singleSwitch : ", botNum, ',', bankNum,',' , switchNum)

def multiSwitch(botNum, bankNum, velocity):
    msgByte = (bankNum << 4) | 64
    msgByte = (velocity << 1) | msgByte
    writeSerial(botNum, msgByte)
    #time.sleep(50)
    print("multiSwitch : ", botNum, ',', bankNum,',' , velocity)

#-------------------------------------------------
#                    Test Loop
#-------------------------------------------------

def test():
    while True:
       randomTest()
       time.sleep(3)
#-------------------------------------------------
#                    Mail Loop
#-------------------------------------------------

receive_address = '127.0.0.1', 40000
osc = OSC.OSCServer(receive_address)
osc.addDefaultHandlers()
osc.addMsgHandler("/switch", switch_handler) # adding our function
# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in osc.getOSCAddressSpace():
    print addr
# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = osc.serve_forever )
st.start()

while 1:
    test()

try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    osc.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
