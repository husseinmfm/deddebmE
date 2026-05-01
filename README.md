# ESP32-CAM Surveillance System

## Overview

This project is a surveillance system that utilizes the ESP32-CAM microcontroller and a Python Flask server to detect motion and inform the user of possible intruders.

## Features

* Motion detection.
* Facial detection and recognition.
* Livestreaming.
* Alerting via Telegram.

## Architecture

1. **ESP32-CAM:**

* Detects motion using a PIR sensor.
* Captures images.
* Sends images to a Flask Python server.
* Livestreams what's presented in front of it if requested.

2. **Flask Server:**

* Receives images sent over by the ESP32-CAM.
* Processes and recognizes the face in the image.
* Compares face to the known faces stored on it.
* Alerts Telegram bot if an unknown face is detected.

3. **Telegram Bot:**

* Receives image from the Flask server.
* Previews image to the user.
* Presents a link to view the ESP32-CAM's live feed.

## Component Requirements

### Hardware

* ESP32-CAM
* OV2640 Camera
* ESP32-CAM Programming Module (to write code on the chip)
* PIR sensor
* PCB
* Battery Holder
* 2x 18650 Li-Ion Batteries
* DC-DC Buck Converter (using multimeter)
* JST Connector

#### Optional:

* Arduino Uno R3 (for calibration of PIR sensor)
* Spacers and Screws (for mounting)

### Software

* Python
* OpenCV
* Flask
* NumPy
* Face_Recognition
* Requests
* Telegram Bot

## Hardware Connection

This is how the connections were made on this specific project.

#### ESP32-CAM Pin Overview

| Function    | ESP32-CAM Pin |
| ----------- | ------------- |
| PIR Signal  | GPIO 3        |
| VCC (Power) | 5V            |
| GND         | GND           |

#### PIR Sensor Connections

| PIR Pin | Connect To ESP32-CAM |
| ------- | -------------------- |
| VCC     | 5V                   |
| GND     | GND                  |
| OUT     | GPIO 3               |

## Setting Up Known Faces

1. Create a `known_faces` folder.
2. Add images of people you want registered.

## Setting Up Telegram Bot

1. Create bot using Telegram's built-in `BotFather`
2. Add bot credentials
3. Request the bot token from `BotFather`
4. Get your chat ID using any of the other various Telegram bots.
5. Start your bot.
6. Enter `Bot_Token` and `Chat_ID` into Python server.

## Setting Up Connection

1. Enter your network's SSID and Password onto the ESP32-CAM while programming it.
2. Enter the server's IP address onto the ESP32-CAM while programming it.
3. Take down the ESP32-CAM's IP address after uploading the code onto it from the serial monitor.
4. Enter the ESP32-CAM's IP address onto the server.
5. Follow the previously mentioned "Setting Up Telegram Bot" steps.
6. Start server.

## Project Flow

1. Motion is detected through the PIR sensor.
2. An image is captured of the object in motion.
3. The image is sent to the Flask server for analysis.
4. The Flask server processes the image.
5. Once a face is recognized, it's compared with the stored known faces.
6. If the face is unknown, the image is sent over to the Telegram bot.
7. A link to the camera's live feed is presented under the image.
8. If pressed, the user's redirected to the ESP32-CAM's livestream.

## Troubleshooting Tips

1. **No Face Detected:**

* Improve lighting.
* Ensure camera isn't obscured.

2. **Telegram Not Sending**

* Verify the bot token and chat ID.
* Make sure your phone is connected to the internet.

3. **ESP32-CAM not Connecting**

* Verify WiFi credentials.
* Check power supply.
* Verify board configuration.

4. **PIR not Detecting Motion**

* Adjust sensitivity using potentiometer.
* Verify ESP32-CAM pin layout.

## Critical Power Note

The ESP32-CAM must be connected to an exactly 5V power supply. Using the 2 18650 Li-Ion batteries on their own could damage the project, so their output voltage must be regulated using a buck converter.
