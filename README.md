# R.A.P.I.D: Remote Automated Patient Image Detection

***Submitted to [MakeUofT 2023](https://devpost.com/software/the-pager-reinvented) by [Gary Zhou](https://garyzhousih.com/), [Joe Dai](https://j0e.ca/), [Samar Qureshi](https://samarq.org/), [Swarnava Ghosh](https://github.com/swarnavaghosh04).***

## Inspiration

In the US alone, over 3 million patients suffer from decubitus ulcers, or bed sores, as a result of sustained pressure being placed on a particular part of the body, from lying down for a prolonged period of time; hospitals in particular, see up to 38% of patients affected by bed sores. It is estimated that the cost of treating pressure ulcers is 2.5 times the cost of preventing them. Our team set out on a mission to solve this issue by prioritizing nurses to frequent patients more often who are bedridden through R.A.P.I.D.

<img src="https://github.com/GaryZhous/MakeUofT/blob/main/RAPID_System.png" title="Components" width=50% height=50%>

## What it does

To avoid bed sores, a patient shouldn’t be stationary for more than two hours. Our sensor module detects if significant movement is made by the patient. If the patient remains still for two hours, a nearby nurse is pinged every 10 minutes until they come and rotate the patient.

## How we built it

Our design is comprised of four modules. The first ESP32 (patient sensor) is equipped with a camera, then sends the video stream over WiFi to our central controller, a Flask server, run on a Raspberry Pi. On a separate ESP8266 (second patient sensor), a gyro sensor detects changes in the patient’s angular velocity, and 2 seconds of continuous positive input from the gyro sensor counts as “patient movement”. The Pi then uses OpenCV to detect the difference in pixels between the video feed, and checks if there is 5 seconds of continuous movement, which counts as “patient movement”. Using sensor fusion with the first ESP32, the Pi detects movement with more depth and precision as opposed to just the single camera.To pull the movement data from the Pi, the M5Stack (another ESP32) pings the Pi every 5 minutes, and will alert the nurse if the patient requires movement. The data is also visualized on the display as separate patient rooms, running on a Flask server, and programmed using Bootstrap (HTML/CSS).

[Check our our project on Devpost!](https://devpost.com/software/the-pager-reinvented)
