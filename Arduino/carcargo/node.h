#ifndef NODE_H
#define NODE_H

//dir 0,1,2,3

// TODO: determine the behavior of each port when occuring a node(here represented as an integer)
#include"track.h"
#include"bluetooth.h"

class Node_Mode: public Tracking_Mode
{
private:
    int i;
    char cmd;
    int dir;
    int l2,l1,m,r1,r2;
    int turn_delay;
    int straight_delay;
    int return_delay;
    //bool need_to_detect;
    int u_delay;
    byte* id;
    byte _idsize;
public:
   Node_Mode();
   bool node_complete;
   bool node_brutal_stop;
   void noding();
   void turn (int dir);
   void moving ();
   bool detect_RFID();
   bool send_RFID();
   bool extra_detect_RFID();
   //bool checking ();
};

Node_Mode::Node_Mode()
{
    i=0;
    cmd = 'n';
    dir = 5;
    l2 = 0;
    l1 = 0;
    m = 0;
    r1 = 0;
    r2 = 0;
    turn_delay = 685; //可以改
    return_delay=700;//7.2V的時候
    straight_delay = 50; //
    u_delay=400;
    node_complete = false;
    //need_to_detect=false;
    node_brutal_stop=false;
    id=0;
    _idsize=0;
}

void Node_Mode::moving()
{
    MotorWriting(200,200);
    delay(straight_delay);
}



void Node_Mode::noding()
{
    do
    {
      MotorWriting(0,0);
      //Serial.println("waiting for a command in node mode");
      get_cmd(cmd);
    }while(cmd!='u' && cmd!='d' && cmd!='r' && cmd!='l' && cmd!='a' && cmd!='h');
    if(cmd=='u'){
      dir=0;
      Serial.println("up");
    }
    else if(cmd=='d'){
      dir=1;
      Serial.println("down");
    }
    else if(cmd=='r'){
      dir=2;
      Serial.println("right");
    }
    else if(cmd=='l')
    {
      dir=3;
      Serial.println("left");
    }
    
    if(cmd=='a')
    {
       node_complete=false;
       node_brutal_stop=true;
    }
    else if(cmd=='h')
    {
      //need_to_detect=false;
      bool detect=false;
      detect=detect_RFID();
      if(!detect)
      {
        MotorWriting(75,75);
        delay(100);
        MotorWriting(0,0);
        detect=detect_RFID();
        if(detect)Serial.println("detect RFID after going ahead");
      }
      if(!detect)
      {
        detect=extra_detect_RFID();
      }
      if(detect) 
      {
        send_RFID();
        //need_to_detect=false;
        Serial.println("detect RFID before turning");
      }
      else
      {
        Serial.println("no rfid");
      }
      node_complete=false;
    }
    else 
    {
       turn(dir);
       dir = 5;
       node_complete=true;
    }
    cmd='n';
}

void Node_Mode::turn(int dir)
{
  unsigned long int time1;
  unsigned long int time2;
  bool detected=false;//確認RFID是否已經偵測並傳出，如果轉完還是沒有傳的話要想個辦法(寫在這個function最下面)
  switch(dir)
  {
  case 0:
    MotorWriting(200,200);
    delay(u_delay);
    break;
  case 1:
    moving();
    MotorWriting(75,75);
    delay(300);
    MotorWriting(-200,200);
    delay(return_delay);
    break;
  case 2:
    moving();
    MotorWriting(0,200);
    delay(turn_delay);
    break;
  case 3:
    moving();
    MotorWriting(200,0);
    delay(turn_delay);
    break;
  }
}

bool Node_Mode::detect_RFID()
{
   id=rfid(&_idsize);
   if(id!=0)return true;
   else if(id==0)return false;
}

bool Node_Mode::send_RFID()
{
   if(id!=0)
   {
       Serial.println('y');
       delay(500);
       for(int i=0;i<_idsize;i++)
       {
          Serial.println(id[i]);
       }
       delay(1000);
       id=0; //把id調回0，下次要偵測的時候才不會混淆
       _idsize=0;
       Serial.println("sent");
       return true;
   }
   return false;
}

bool Node_Mode::extra_detect_RFID()
{
    bool detect=false;
    Serial.println("extra detect");
    for(int i=0;i<3;i++)
    {
      MotorWriting(75,75);
      delay(100);
      MotorWriting(0,0);
      detect=detect_RFID();
      if(detect) return true;
      MotorWriting(-75,-75);
      delay(100);
      MotorWriting(0,0);
      detect=detect_RFID();
      if(detect) return true;
    }
    return false;
}

#endif
