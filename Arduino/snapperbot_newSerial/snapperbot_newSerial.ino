//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// Firmware for the SnapperBot
// by Nathan Villicana-Shaw
// Spring 2015
// CalArts MTIID
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

// supports uint8_t and uint16_t
#include <stdint.h>
// Definition of interrupt names
#include <avr/interrupt.h>
// ISR interrupt service routine
#include <avr/io.h>
//for better readability
#define unit8_t FLIP 0
#define unit8_t LOUD 1
#define unit8_t VERY 2
//for communicatoin
#include <Wire.h>
// PORTA, PORTB, PORTC, PORTL
static int snapper1[8] = {22, 23, 24, 25, 26, 27, 28, 29};
static int snapper2[8] = {10, 11, 12, 13, 50, 51, 52, 53};
static int snapper3[8] = {30, 31, 32, 33, 34, 35, 36, 37};
static int snapper4[8] = {42, 43, 44, 45, 46, 47, 48, 49};
//the states of the snappers
uint8_t snapperStates[4];
//the incomming messages
byte dataBytes[3];
//for parsing serial
uint8_t mode;
uint8_t botNum;
//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                              i2c functions
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
void sendI2C(uint8_t _botNum, uitn8_t _msgType, uint8_t _dataByte) {
  //start i2c message to slavebot _botNum
  Wire.beginTransmission(_botNum);
  //write byte to slavebot
  Wire.write(_msgType);
  Wire.write(_dataByte);
  //close i2c message, if we wanted to send more info we would add another Wire.write
  Wire.endTransmission();
}
//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                        Intrument Commands
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
void setPorts(uint8_t which) {
  if (which == 0) {
    PORTA = snapperStates[0];
  }
  else if (which == 1) {
    PORTB = snapperStates[1];
  }
  else if (which == 2) {
    PORTC = snapperStates[2];
  }
  else if (which == 3) {
    PORTL = snapperStates[3];
  }
  else if (which == 4) {
    PORTA = snapperStates[0];
    PORTB = snapperStates[1];
    PORTC = snapperStates[2];
    PORTL = snapperStates[3];
  }
}
//
void flipSwitch(uint8_t array, uint8_t swit) {
  uint8_t mask;
  mask = 1 << (swit - 1);
  snapperStates[array] = snapperStates[array] ^ mask;
  setPorts(array);
}
//
void veryLoud(uint8_t bankNum, uint8_t level) {
  for (int i = 0; i < bankNum; i++) {
    snapperStates[i] ^= (255 >> (8 - level));
    setPorts(i);
  }
}
//
void loud(uint8_t snapArray, uint8_t level) {
  snapperStates[snapArray] ^= (255 >> (8 - level));
  setPorts(snapArray);
}
//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                              Serial Stuff
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
byte tempByte, msgID, botNum, arrayNum, switNum;

void byteListener() {
  while (Serial.available()) {
    if (Serial.available()) {
      while (!Serial.available()) {};
      byte tempByte = Serial.read();
      //if we have a flag bit
      if (tempByte & 0x80 == 0x80) {
        botNum = tempByte & 0x7;
        switch (tempByte & 0x30) {
          case 0:
            if (botNum == 0) {
              tempByte = Serial.read();
              arrayNum = tempByte & 0x30;
              switNum = tempByte & 0xF;
              flipSwitch(arrayNum, switNum);
            }
            else {
              tempByte = Serial.read();
              sendI2C(botNum, 0, tempByte);
            }
            break;

          case 1:
            if (botNum == 0) {
              tempByte = Serial.read();
              arrayNum = tempByte & 0x30;
              switNum = tempByte 7 0xF;

              loud(arrayNum, switchNum);
            }
            else {
              tempByte = Serial.read();
              sendI2C(botNum, 1, tempByte);
            }
            break;

          case 2:
            if (botNum == 0) {
              tempByte = Serial.read();
              arrayNum = tempByte & 0x30;
              switNum = tempByte & 0xF;
              veryLoud(arrayNum, switNum);
            }
            else {
              tempByte = Serial.read();
              sendI2C(botNum, 2, tempByte);
            }
            break;

          case 3:
            break;
        }
      }
    }
  }
}
//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                             Test Loops
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
//flip a random switch on a random array
void randomFlipTest() {
  flipSwitch(random(0, 4), random(0, 8));
}
//send random messages to salvebots to test iic
void startupTest() {
  for (uint8_t i = 0; i < 6; i++) {
    if (i == 0) {
      for (int t = 1; t < 9; t++) {
        for (int i = 0; i < 4; i++) {
          loud(i, t);
          delay(13);
        }
      }
      for (int i = 1; i < 9; i++) {
        veryLoud(i);
        delay(27);
      }
    }
    else {
      for (uint8_t t = 30; t < 225; t++) {
        sendI2C(i, t);
        delay(3);
      }
    }
  }
}
//test a specific slavebot
void testBot(int botNum, int time) {
  for (int i = 0; i < 255; i++) {
    sendI2C(botNum, i);
    delay(time);
  }
}
//test a specific switch on a slavebot
void testSwitch(int botNum, int switchNum) {
  sendI2C(botNum, switchNum);
}
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                             Setup Loop
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
void setup() {
  Serial.begin(9600);
  //open i2c port
  Wire.begin();//no address given, which designates this bot as master device on iic bus
  //set all pins as output pins
  for (int i = 0; i < 8; i++) {
    pinMode(snapper1[i], OUTPUT);
    pinMode(snapper2[i], OUTPUT);
    pinMode(snapper3[i], OUTPUT);
    pinMode(snapper4[i], OUTPUT);
  }
  //set them all to high (which is off for the switches)
  for (int i = 0; i < 4; i++) {
    snapperStates[i] = 0xFF;
  }
  //write to all the ports at the same time
  setPorts(4);
  startupTest();
}
//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                               Main Loop
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//

//keep it clean baby!
void loop() {
  byteListener();
}
