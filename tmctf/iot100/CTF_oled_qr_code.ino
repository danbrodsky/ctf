#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
#include "SSD1306Wire.h"
#include "qrcode.h"

#define SECRET "" //put your secret code here

void setup() {
  
SSD1306Wire  display(0x3c, D3, D5);
display.init();
display.setColor(WHITE);

// Create the QR code 29x29
    QRCode qrcode;
    uint8_t qrcodeData[qrcode_getBufferSize(3)];
    qrcode_initText(&qrcode, qrcodeData, 3, 0, SECRET);


for (uint8_t y = 0; y < qrcode.size; y++) {
        // Each horizontal module
        for (uint8_t x = 0; x < qrcode.size; x++) {
           if(qrcode_getModule(&qrcode, x, y)){
            display.setPixel(x, y);

           }
        }
 }

display.display();
}

void loop() {
  // put your main code here, to run repeatedly:

}
