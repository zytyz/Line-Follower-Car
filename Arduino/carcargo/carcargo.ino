#include<SoftwareSerial.h>

#include "track.h"
#include "node.h"
#include "bluetooth.h"

enum ControlState 
{
   START_STATE,
   TRACKING_STATE,
   NODE_STATE,
};

// global variable
ControlState _state;               // Control State
char  _state_cmd = 'n';                        // Command
char _brutalstop='x';
Tracking_Mode carcartrack;
Node_Mode carcarnode;

// function
void Start_Mode();
//void MotorWriting(double& vR, double& vL);
void SetState();

void setup()
{
    Serial.begin(9600);
    I2CBT.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init();
    pinMode(MotorL_I1,   OUTPUT);
    pinMode(MotorL_I2,   OUTPUT);
    pinMode(MotorR_I3,   OUTPUT);
    pinMode(MotorR_I4,   OUTPUT);
    pinMode(MotorR_PWMR, OUTPUT);
    pinMode(MotorL_PWML, OUTPUT);
    pinMode(R1, INPUT); 
    pinMode(R2, INPUT);
    pinMode(M,  INPUT);
    pinMode(L1, INPUT);
    pinMode(L2, INPUT);
    _state = START_STATE;      // Control State
    Serial.println("Start!");
    
}


void loop()
{
      I2CBT.write("hiiii");
      //Serial.println("oop");
      if(_state == START_STATE) Start_Mode();
      else if(_state == TRACKING_STATE) carcartrack.track();
      else if(_state == NODE_STATE) carcarnode.noding();
      SetState();
}

void SetState()
{
  
   if(_state == START_STATE) 
   {
      Serial.println('z');
      get_cmd(_state_cmd);
      if (_state_cmd == 's') {
          _state = TRACKING_STATE;
          Serial.print("_state_cmd: ");
          Serial.println('s');
          Serial.println("Start Tracking !!"); 
          _state_cmd = 'n';
      }
      else { _state = _state; }
   }
   else if(_state == TRACKING_STATE){
      if(carcartrack.detect_node()){
         _state = NODE_STATE;
         //BTsend('q');
         Serial.println("Start noding !!"); 
      }
      else if(carcartrack.BrutalStop())
      {
          _state = START_STATE;
          Serial.println("Stop and set to start mode");
          carcartrack.brutalcmd='x';
      }
      else { _state = _state; }
   }
   else if( _state == NODE_STATE){
      if(carcarnode.node_complete){
         _state = TRACKING_STATE;
         carcarnode.node_complete=false;
         Serial.println("Tracking Again!!"); 
      }
      else if(carcarnode.node_brutal_stop==true)
      {
          _state = START_STATE;
          Serial.println("Stop and set to start mode");
          carcarnode.node_brutal_stop=false;
      }
      else { _state = _state; }
   }
}

void Start_Mode() {
   analogWrite(MotorR_PWMR,0);
   analogWrite(MotorL_PWML,0);
   digitalWrite(MotorL_I1,LOW);
   digitalWrite(MotorL_I2,LOW);
   digitalWrite(MotorR_I3,LOW);
   digitalWrite(MotorR_I4,LOW);
   carcartrack.MotorWriting(0,0);
}


