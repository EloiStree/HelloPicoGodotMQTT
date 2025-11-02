# HelloPicoGodotMQTT
Let's learn how to use MQTT to make connection between Pico 2W ESP32 and Godot Engine.


I need for my project to link a game to hundreds of Pico 2W to make code tournament.
I could design the concept with UDP and Websocket.

But MQTT is easy to use and if Godot on the Asset Library works on all platform, it could be a good solution.


So let's learn how to host a MQTT server On Raspberry Pi 5 and on Window.


Update your system and install mosquito:   
```
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
```
