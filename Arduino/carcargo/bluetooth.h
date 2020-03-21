#ifndef BLUETOOTH_H
#define BLUETOOTH_H

#include<SoftwareSerial.h>
#include "RFID.h"

SoftwareSerial I2CBT(8,1);   //bluetooth RX,TX
// TODO: return the direction based on the command you read

void get_cmd(char &_cmd)
{
   delay(50); 
   if(I2CBT.available())
   {
    _cmd=I2CBT.read();
    Serial.print("Cmd: ");
    Serial.println(_cmd);
   }
}

void BTsend(char c)
{
    //I2CBT.write(c);
    Serial.println(c);
}
#endif

