#ifndef TRACK_H
#define TRACK_H

#include "bluetooth.h"

#define MotorL_I1     7  //定義 I1 接腳 
#define MotorL_I2     6  //定義 I2 接腳
#define MotorR_I3     5  //定義 I3 接腳 
#define MotorR_I4     4 //定義 I4 接腳
#define MotorR_PWMR    3  //定義 ENB (PWM調速) 接腳 
#define MotorL_PWML    9  //定義 ENA (PWM調速) 接腳 

#define R2  A4  // Define Second Right Sensor Pin
#define R1  A3  // Define First Right Sensor Pin
#define M   A2  // Define Middle Sensor Pin
#define L1  A1  // Define First Left Sensor Pin
#define L2  A0  // Define Second Leftt Sensor Pin


class Tracking_Mode
{
private:
  //int detect_black; //一個參數 用來偵測node的黑線 避免車子一歪就暫停
protected:                      
  int l2, l1, m, r1, r2;
  /*int last_l2;
  int last_l1;
  int last_m;
  int last_r1;
  int last_r2;*/
  double _Tp ;                         // Velocity of Car
  double _w2 ;                       // Weight Value for the Outer Sensor
  double _w1 ;                   // Weight Value for the Inner Sensor
  double _Kp ;                       // _Kp Parameter
  double _Kd ;                        // _Kd Parameter
  double _Ki ;                         // _Ki Parameter
  double _LastError ;  
  double _integral ;                     // Integral from Starting point
  bool R_dir ;                        // if dir == ture, mean right-motor is forwarding. On the other hand, backwarding.
  bool L_dir ; 
public:
  char brutalcmd;
  Tracking_Mode();
  void track();//shin gee
  void MotorWriting(double vR, double vL);
  bool detect_node();
  bool BrutalStop();
};

Tracking_Mode::Tracking_Mode(){
  //detect_black = 1;                         //一個參數 用來偵測node的黑線 避免車子一歪就暫停
  brutalcmd='x';
  l2 = 0;
  l1 = 0;
  m = 0;
  r1 = 0;
  r2 = 0;
  _Tp = 60;                         // Velocity of Car
  _w2 = 2 ;                       // Weight Value for the Outer Sensor
  _w1 = _w2/2.0;                     // Weight Value for the Inner Sensor
  _Kp = 60;                          // _Kp Parameter
  _Kd = 0.03;                        // _Kd Parameter
  _LastError = 0;  
  _Ki = 6.0;                         // _Ki Parameter
  _integral = 0;                     // Integral from Starting point
  R_dir = true;                        // if dir == ture, mean right-motor is forwarding. On the other hand, backwarding.
  L_dir = true; 
}



void Tracking_Mode::track() 
{
    //Serial.println("track now"); 
    l2=digitalRead(L2);
    l1=digitalRead(L1);
    m=digitalRead(M);
    r1=digitalRead(R1);
    r2=digitalRead(R2);
    _Tp = 60;
    double error=_w2*l2+_w1*l1-_w2*r2-_w1*r1;           
    if((l1+l2==2)||(l1+m==2)||(r1+m==2)||(r1+r2==2))error=error/2; 
    double revise = 4/5;                                           //need to test
    _integral = revise*_integral + error;      
    if(error>=1.5) _Tp=0;      
    double power=_Kp*error + _Ki*_integral;
    double vR=_Tp+power;
    double vL=_Tp-power; 
    MotorWriting((int)vR, (int)vL);      
}

bool Tracking_Mode::BrutalStop()
{
    get_cmd(brutalcmd);
    if(brutalcmd=='a')
    {
      MotorWriting(0,0);
      return true;
    }
    else return false;
}

void Tracking_Mode::MotorWriting(double vR, double vL) 
{
   analogWrite(MotorL_PWML,0);
   analogWrite(MotorR_PWMR,0);
   if(vL<0)
   {
       digitalWrite(MotorL_I2,LOW);
       digitalWrite(MotorL_I1,HIGH);
       vL=-vL;
   }
   else
   {
        digitalWrite(MotorL_I1,LOW);
        digitalWrite(MotorL_I2,HIGH);
   }
   analogWrite(MotorL_PWML,vL);
   if(vR<0){
       digitalWrite(MotorR_I4,LOW);
       digitalWrite(MotorR_I3,HIGH);
       vR=-vR;
   }
   else{
      digitalWrite(MotorR_I3,LOW);
      digitalWrite(MotorR_I4,HIGH);
   }
   analogWrite(MotorR_PWMR,vR);
}   

bool Tracking_Mode::detect_node()//黑線是1 白線是0
{
    bool i;
	  l2=digitalRead(L2);
    l1=digitalRead(L1);
    m=digitalRead(M);
    r1=digitalRead(R1);
    r2=digitalRead(R2);
    if ( l2 + l1 + m + r1 + r2 >= 3)
    {
      if (l2 + l1 + m + r1 + r2 == 5)  i=true;
      else if (l2 + l1 + m + r1 + r2 == 4)
      {
        if (l2==0)  i=true;
        else if (r2==0)  i=true;
      }
      else if (l2 + l1 + m + r1 + r2 == 3)
      {
        if (l2==0&&l1==0)  i=true;
        else if (r2==0&&r1==0)  i=true;
      }
    }
    else i=false;
    if (i)
    {  
      MotorWriting(0,0);
      //delay(1000);
      Serial.println('q');
      return true;
    }
    else 
    {
      //Serial.println('q');
      //return true;
      return false;
    }
}

#endif
