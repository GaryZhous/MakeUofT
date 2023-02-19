#include <Arduino.h>
#include <M5Stack.h>
#include "WiFi.h"
// #include "ESPAsyncWebServer.h"
#include "HTTPClient.h"
#include "ESP32Time.h"

extern void initWiFi();
extern void displaypower();
extern bool needmove();
extern void warn();
//set the frequency of the speaker (unit: Hz)
enum frequency{
  F1 = 200,
  F2 = 300,
  F3 = 400,
  F4 = 500,
  F5 = 900
};

const char* ssid = "RAPID";
const char* password = "helloworld";
ESP32Time rtc(3600);
int timing;
int next = 1;
void setup() {
    Serial.begin(115200);
    M5.begin();    
    M5.Power.begin(); 
    M5.Lcd.setTextSize(2);
    M5.lcd.setCursor(25,100);
    WiFi.mode(WIFI_AP);
    WiFi.disconnect();
    delay(100);
    initWiFi();
    timing = rtc.getMinute();
}

void loop() {
    M5.update();
    int curr_time = rtc.getMinute();
    if(M5.BtnA.wasPressed())
      next = -next;
    if(curr_time - timing == 1){
       if(needmove && next < 0){
         M5.Lcd.setCursor(25, 100);
         M5.Lcd.println("Need Move!");
         M5.Speaker.tone(F5);
       }
       timing = curr_time;
    }
    int fren[] = {F1,F2,F3,F4,F5};
    M5.Lcd.setCursor(25, 100);
    if(M5.BtnB.wasPressed()){
        M5.Lcd.println("Beeping activated");
        M5.Speaker.tone(fren[rand()%5], 200); //200 miliseconds ringing
    }else if(M5.BtnC.wasPressed()){
        M5.Lcd.println("Stop button was pressed!");
        M5.Speaker.end();
        delay(500);
        M5.lcd.clear();
        displaypower();
    }
}

void initWiFi() {
  int count = 0;
  WiFi.mode(WIFI_AP);
  WiFi.begin(ssid, password);
  M5.Lcd.setCursor(25, 100);
  M5.Lcd.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED && count++ < 10) {
    M5.Lcd.println('.');
    delay(1000);
  }
  M5.Lcd.clear();
  M5.Lcd.setCursor(25, 100);
  if(count < 10)
    M5.Lcd.println("Ready!");
  else
    M5.Lcd.println("Failed to connect!");
}

bool needmove() {
  HTTPClient http;
  http.begin("http://10.0.0.1:8080/api/need_move/100");
  int code = http.GET();
  if (code == HTTP_CODE_OK) {
    String resp = http.getString();
    if (resp == "Need move!") {
      return true;
    }
    else {
      return false;
    }
  }
  return false;
}

void displaypower(){
  char buf[100];
  sprintf(buf, "Current battery: %d%c", M5.Power.getBatteryLevel(), (char)37);
  M5.Lcd.setCursor(25, 90);
  M5.Lcd.println(buf);
  sprintf(buf, "%s", M5.Power.isCharging() ? "Charging!" : "Discharging!");
  M5.Lcd.setCursor(25, 110);
  M5.Lcd.println(buf);
  delay(1000);
  M5.Lcd.clear();
}