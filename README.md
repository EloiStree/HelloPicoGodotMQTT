# Hello Pico Godot MQTT

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
# === GLOBAL SETTINGS ===
per_listener_settings true
log_type all
connection_messages true
log_dest syslog
log_dest stdout
pid_file /var/run/mosquitto.pid

# === LISTENER 1: Anonymous (port 1883) ===
listener 1883 0.0.0.0
allow_anonymous true
acl_file /etc/mosquitto/aclfile

# === LISTENER 2: Authenticated (port 1884) ===
listener 1884 0.0.0.0
allow_anonymous false
password_file /etc/mosquitto/passwd
acl_file /etc/mosquitto/aclfile

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
# If you allows player to send you information.
# topic write game_input/#

# Guests can READ game data
topic read game_data/#


# -----------------------------
# ACLs for Admins (authenticated users)
# -----------------------------
user admin
topic readwrite game_data/#
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



```
sudo chmod 644 /etc/mosquitto/mosquitto.conf
sudo chown root:root /etc/mosquitto/mosquitto.conf
sudo chmod 644 /etc/mosquitto/aclfile

sudo mkdir -p /var/run
sudo chown mosquitto:mosquitto /var/run

sudo chown mosquitto:mosquitto /etc/mosquitto/passwd /etc/mosquitto/aclfile
sudo chmod 600 /etc/mosquitto/passwd
sudo chmod 644 /etc/mosquitto/aclfile

sudo systemctl restart mosquitto

journalctl -u mosquitto -f

mosquitto -c /etc/mosquitto/mosquitto.conf -v
```






