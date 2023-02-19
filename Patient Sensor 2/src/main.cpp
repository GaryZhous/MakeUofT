#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define LED_PIN 16

Adafruit_MPU6050 mpu;
HTTPClient http;
WiFiClient wifi;
int triggered = 0;

void sendRequest() {
  http.begin(wifi, "http://10.0.0.1:8080/api/moved/100");
  http.GET();
  http.end();
}

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  Serial.println("");

  pinMode(LED_PIN, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin("RAPID", "helloworld");
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_PIN, LOW);
    delay(100);
    digitalWrite(LED_PIN, HIGH);
    delay(100);
  }
}

void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  double x = 0, y = 0, z = 0;
  for (int n = 0; n < 50; n++) {    // 250 ms averaging
    x += g.gyro.x;
    y += g.gyro.y;
    z += g.gyro.z;
    delay(5);
  }
  x /= 50;
  y /= 50;
  z /= 50;
  x = abs(x);
  y = abs(y);
  z = abs(z);
  Serial.println(x);
  Serial.println(y);
  Serial.println(z);

  if (x > 0.8 || y > 0.8 || z > 0.8) {
    digitalWrite(LED_PIN, LOW);
    Serial.println("Movement!");
    triggered += 1;
  }
  else {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("No movement.");
    triggered = 0;
  }

  if (triggered >= 8) {    // 2 s min
    sendRequest();
    for (int i = 0; i < 10; i++) {
      digitalWrite(LED_PIN, LOW);
      delay(25);
      digitalWrite(LED_PIN, HIGH);
      delay(25);
    }
    triggered = 0;
  }
}
