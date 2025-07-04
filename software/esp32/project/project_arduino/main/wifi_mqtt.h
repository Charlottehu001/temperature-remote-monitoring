#ifndef WIFI_MQTT_H
#define WIFI_MQTT_H

#include <WiFi.h>
#include <PubSubClient.h>

extern WiFiClient espClient;
extern PubSubClient mqttClient;

// WiFi connection setup
void connectWiFi();

// MQTT connection setup
void connectMQTT();

// MQTT message sending function
void sendMQTTMessage(const char *topic, const char *payload);

// MQTT message receiving callback function type
typedef void (*MQTTCallback)(char* topic, byte* payload, unsigned int length);

// Set MQTT message receiving callback function
void setMQTTCallback(MQTTCallback callback);

// Subscribe to MQTT topic
void subscribeMQTTTopic(const char *topic);

// MQTT client loop processing
void mqttLoop();

#endif // WIFI_MQTT_H
