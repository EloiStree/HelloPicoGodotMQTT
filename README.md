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
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
sudo systemctl status mosquitto

```

```
sudo rm /etc/mosquitto/mosquitto.conf
sudo nano /etc/mosquitto/mosquitto.conf
```

```
# ========================
# Mosquitto Configuration
# ========================

# --- Guest listener (limited to 16 bytes) ---
listener 1883 0.0.0.0
allow_anonymous true
acl_file /etc/mosquitto/aclfile
message_size_limit 16
log_type all
connection_messages true
log_dest syslog
log_dest stdout

# --- Admin listener (full access) ---
listener 1884 0.0.0.0
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/aclfile
log_type all
connection_messages true
log_dest syslog
log_dest stdout

```

Enter a password:
(would be better with crypto login but for beginner password is ok)
```
sudo mosquitto_passwd -c /etc/mosquitto/passwd admin
```


Config of write read;
```
sudo nano /etc/mosquitto/aclfile
```

```
# -----------------------------
# ACLs for Guests (anonymous)
# -----------------------------

# Guests can PUBLISH game input
topic write game_input/#

# Guests can READ game data
topic read game_data/#


# -----------------------------
# ACLs for Admins (authenticated users)
# -----------------------------
user admin
topic write game_data/#
topic read game_input/#
topic readwrite $SYS/#
```

```
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

```
mosquitto_sub -h localhost -t test/topic -u myuser -P mypassword
```

