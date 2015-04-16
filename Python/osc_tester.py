import OSC, random, time
c = OSC.OSCClient()
c.connect("10.0.1.5", 40000)
while 1 :
	oscmsg = OSC.OSCMessage()
	oscmsg.setAddress("/switch")
	oscmsg.append(0)
	oscmsg.append(random.randint(0,3))
	oscmsg.append(random.randint(1,8))
	c.send(oscmsg)
	time.sleep(0.5)
	print(oscmsg)
