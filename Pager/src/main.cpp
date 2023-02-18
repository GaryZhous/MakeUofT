#include <Arduino.h>
#include <M5Stack.h>
//set the frequency of the speaker (unit: Hz)
enum frequency{
  F1 = 200,
  F2 = 300,
  F3 = 400,
  F4 = 500,
  F5 = 900
};

void setup() {
    M5.begin();    
    M5.Power.begin(); 
    M5.Lcd.setTextSize(2);
    M5.lcd.setCursor(25,100);
    M5.lcd.println("Ready!");
}

void loop() {
    M5.update();
    int fren[] = {F1,F2,F3,F4,F5};
    M5.Lcd.setCursor(25, 100);
    if (M5.BtnA.wasPressed()) {
        M5.Lcd.println("Beeping activated");
        M5.Speaker.tone(fren[rand()%5], 200); //200 miliseconds ringing
    } else if (M5.BtnB.wasPressed()) {
        M5.Lcd.println("Buzz mode activated");
        M5.Speaker.tone(F5); //keep buzzing
    } else if (M5.BtnC.wasPressed()) {
        M5.Lcd.println("Stop button was pressed!");
        M5.Speaker.end();
        delay(500);
        M5.lcd.clear();
    }
}
