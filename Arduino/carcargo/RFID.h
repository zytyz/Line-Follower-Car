#ifndef RFID_H
#define RFID_H

#include <SPI.h>
#include <MFRC522.h>     // 引用程式庫
/* pin---- SDA:9 SCK:13 MOSI:11 MISO:12 GND:GND RST:9  */

#define RST_PIN      A5        // RFID resetpin
#define SS_PIN       10      // RFID selection pin
MFRC522 mfrc522(SS_PIN, RST_PIN);  // MFRC522 object declaration

byte* rfid(byte* idSize) //return the pointer of the array that stores each byte of the id (the length of the array is *idSize)
{
    // 確認是否有新卡片
    //Serial.println("in the rfid function");
    bool tmp=mfrc522.PICC_IsNewCardPresent();
    bool tmp2=mfrc522.PICC_ReadCardSerial();
    //Serial.println(tmp);
    //Serial.println(tmp2);
    if (tmp && tmp2)   //mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) 
    {
        //Serial.println("yeah");
        byte *id = mfrc522.uid.uidByte;   // 取得卡片的UID
        *idSize = mfrc522.uid.size;   // 取得UID的長度
  
        //Serial.print("PICC type: ");      // 顯示卡片類型
        // 根據卡片回應的SAK值（mfrc522.uid.sak）判斷卡片類型
        MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
        /*Serial.println(mfrc522.PICC_GetTypeName(piccType));
  
        //Serial.print("UID Size: ");       // 顯示卡片的UID長度值
        //Serial.println(idSize);

        for (byte i = 0; i < *idSize; i++) {  // 逐一顯示UID碼
          Serial.print("id[");
          Serial.print(i);
          Serial.print("]: ");
          Serial.println(id[i], HEX);       // 以16進位顯示UID值  
        }
      
        Serial.println();*/
  
        mfrc522.PICC_HaltA();  // 讓卡片進入停止模式
        return id;
    }
    //delay(100);
    return 0;
}

#endif
