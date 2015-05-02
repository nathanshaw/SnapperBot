//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// Firmware for the SnapperBot
// by Nathan Villicana-Shaw
// Spring 2015
// CalArts MTIID
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
// supports uint8_t and uint16_t
#include <stdint.h>
// Definition of interrupt names
#include <avr/interrupt.h>
// ISR interrupt service routine
#include <avr/io.h>
//
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
//
uint8_t snapperStates[4];//the states of the snappers
//the incomming messages
uint8_t incommingByte;
//for parsing serial
uint8_t mode;

//
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                              i2c functions
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//

//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                             Setup Loop
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//
void setup() {
  //this means the address for the arduino is now 1, and it is a slave
  Wire.begin(4);
  Wire.onReceive(triggerEvent);//when the arduino receives a message on its Serial port it will forward the data to the receiveEvent event function
  //set all pins as output pins
  for (int i = 0; i < 8; i++) {
    pinMode(snapper1[i], OUTPUT);
    pinMode(snapper2[i], OUTPUT);
    pinMode(snapper3[i], OUTPUT);
    pinMode(snapper4[i], OUTPUT);
  }
  //set them all to high (which is low on the snapper arrays)
  for (int i = 0; i < 4; i++) {
    snapperStates[i] = 0xFF;
  }
  //write to all the ports at the same time
  setPorts(4);
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

void allOff(){
 for(int i; i < 4; i++){
  snapperStates[i] = 0xFF;
 } 
}

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
void triggerEvent(int port) {
  //if we have serial data in the buffer
  if (Wire.available()) {
    //and as long as we have bytes to be read
    while (Wire.available()) {
      //parse out the data one byte at a time
      parseI2C(Wire.read(), Wire.read());
    }
  }
}
//
void parseI2C(uint8_t mode, uint8_t data) {
    //flip one switch is mode is = 0
    if (mode == 1) {
      //apply bitmasks and shift over the bits we are interested in and pass them into flipSwitch
      flipSwitch((data & 0x30) >> 4,  (data & 0xF));
    }
    else if (mode == 2) {
      //apply bitmasks and shift over the bits we are interested in and pass them into loud
      loud((data & 0x30) >> 4, data & 0xF);
    }
    else if (mode == 3) {
      //apply bitmasks and shift over the bits we are interested in and pass them into veryLoud
      veryLoud((data & 0x30) >> 4, data & 0xF);
    }
    else if (mode == 4){
     allOff(); 
    }
}

//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//                               Main Loop
//////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
//

//everything is evert driven so no need for anything in the loop
void loop() {
}
