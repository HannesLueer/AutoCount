# AutoCount
AutoCount is a camera-based system for automatic car counting in indoor parking facilities that was developed as a student project.
A camera placed at the entrance of the parking facility captures footage for object recognition, focusing only on cars entering and exiting. 
This minimizes the probability of unwanted objects or people being detected, in contrast to using a light curtain.

## Implementation
As Hardware we used a Raspberry Pi 3 and a Raspberry Pi Camera version 2.1 for this project. 

The system developed in this project consists of three subsystems: the [sensor](https://github.com/HannesLueer/AutoCount/tree/main/sensor), the [server](https://github.com/HannesLueer/AutoCount/tree/main/server), and the [app](https://github.com/HannesLueer/AutoCount/tree/main/frontend). 
The sensor system replaces traditional detection methods, while the server acts as a communication link between the sensor and the app. 
The app presents the collected data to the user, sent from the server.

![software architecture](https://raw.githubusercontent.com/HannesLueer/AutoCount/main/documentation/Bilder/Architektur_gesamt_2.svg)

The sensor component is developed using Python with different approaches to detect the direction of cars (see [method 'direction of the movement vector'](https://github.com/HannesLueer/AutoCount/tree/main/sensor/src/car_detection_method_2) and [method 'crossing a line'](https://github.com/HannesLueer/AutoCount/tree/main/sensor/src/car_detection_method_3)). 
Data from the sensor is transmitted to the server using HTTP.
The server, implemented in Go, utilizes SQLite for database management.
It offers both MQTT and HTTP for data communication to clients.
On the client side, the mobile app is developed with Flutter, which subscribes to the server's MQTT broker.

A complete documentation in German is available as a [PDF file](https://github.com/HannesLueer/AutoCount/blob/main/documentation/Arbeit.pdf), as well as a [video](https://github.com/HannesLueer/AutoCount/tree/main/video) promoting this system.
