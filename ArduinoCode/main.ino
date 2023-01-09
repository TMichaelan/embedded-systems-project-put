#include "ArduinoJson.h"
#define PIN_DIRECTION_RIGHT 3
#define PIN_DIRECTION_LEFT  4
#define PIN_MOTOR_PWM_RIGHT 5
#define PIN_MOTOR_PWM_LEFT  6

StaticJsonDocument<200> jsondoc;

int16_t speedA = 0;
int16_t speedB = 0;


void setup() {
  Serial.begin(9600);
  pinMode(PIN_DIRECTION_LEFT, OUTPUT);
  pinMode(PIN_MOTOR_PWM_LEFT, OUTPUT);
  pinMode(PIN_DIRECTION_RIGHT, OUTPUT);
  pinMode(PIN_MOTOR_PWM_RIGHT, OUTPUT);
}

void loop() {
  DeserializationError err = deserializeJson(jsondoc, Serial);  
  if (err == DeserializationError::Ok)    
  {
    speedA = (float)jsondoc["speedA"] * 2;  //  range [-100; 100]
    speedB = (float)jsondoc["speedB"] * 2;  // expand to [-255; 255]
  }
  else
  {
    while (Serial.available() > 0) Serial.read(); 
  }
  //moveA(speedA);  // update moror speed
  //(speedB);  //
  delay(10);

  motorRun(speedA,speedB);

// //Move forward
//  motorRun(200, 200);
//  delay(1000);
//
//  //Move back
//  motorRun(-200, -200);
//  delay(1000);
//
//  //Turn left
//  motorRun(-200, 200);
//  delay(1000);
//
//  //Turn right
//  motorRun(200, -200);
//  delay(1000);
//
//  //Stop
//  motorRun(0, 0);
//  delay(2000);


  
}

void motorRun(int speedl, int speedr) {
  int dirL = 0, dirR = 0;
  if (speedl > 0) {
    dirL = 0;
  }
  else {
    dirL = 1;
    speedl = -speedl;
  }
  if (speedr > 0) {
    dirR = 1;
  }
  else {
    dirR = 0;
    speedr = -speedr;
  }
  digitalWrite(PIN_DIRECTION_LEFT, dirL);
  digitalWrite(PIN_DIRECTION_RIGHT, dirR);
  analogWrite(PIN_MOTOR_PWM_LEFT, speedl);
  analogWrite(PIN_MOTOR_PWM_RIGHT, speedr);
}
