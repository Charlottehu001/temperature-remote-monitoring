#include <WiFi.h>
#include <PubSubClient.h>
#include "wifi_mqtt.h"

// WiFi and MQTT client objects
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// WiFi settings
const char *ssid = "CHARLOTTE";					// Change to your WiFi SSID
const char *password = "413Rm44]"; // Change to your WiFi password

// MQTT settings
const char *mqtt_server = "192.168.178.3"; // MQTT server address
const int mqtt_port = 1883;									 // MQTT port
const char *mqtt_user = "username";					 // MQTT username
const char *mqtt_pass = "password";					 // MQTT password

// WiFi connection function
void connectWiFi()
{
	Serial.print("Connecting to WiFi...");
	WiFi.begin(ssid, password);

	while (WiFi.status() != WL_CONNECTED)
	{
		delay(1000);
		Serial.print(".");
	}

	Serial.println("Connected to WiFi");
}

// MQTT connection function
void connectMQTT()
{
	mqttClient.setServer(mqtt_server, mqtt_port);
	while (!mqttClient.connected())
	{
		Serial.print("Connecting to MQTT...");

		if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_pass))
		{
			Serial.println("Connected to MQTT");
		}
		else
		{
			Serial.print("Failed, rc=");
			Serial.print(mqttClient.state());
			Serial.println(" try again in 5 seconds");
			delay(5000);
		}
	}
}

// MQTT message sending function
void sendMQTTMessage(const char *topic, const char *payload)
{
	if (!mqttClient.connected())
	{
		connectMQTT();
	}
	mqttClient.publish(topic, payload);
}

// Set MQTT message receiving callback function
void setMQTTCallback(MQTTCallback callback)
{
	mqttClient.setCallback(callback);
}

// Subscribe to MQTT topic
void subscribeMQTTTopic(const char *topic)
{
	if (!mqttClient.connected())
	{
		connectMQTT();
	}
	mqttClient.subscribe(topic);
	Serial.print("Subscribed to topic: ");
	Serial.println(topic);
}

// MQTT client loop processing
void mqttLoop()
{
	if (!mqttClient.connected())
	{
		connectMQTT();
	}
	mqttClient.loop();
}
