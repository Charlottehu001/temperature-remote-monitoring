#include <WiFi.h> // Library for WLAN functionality
#include <PubSubClient.h> // Library for MQTT communication

// WLAN access data
const char *ssid = "DuRuofu_ESP32"; // WLAN network name
const char *password = "3.1415926"; // WLAN password

// MQTT broker configuration
const char *mqtt_broker = "192.168.154.109"; // Local IP address of MQTT broker (on laptop)
const char *topic = "test"; // MQTT topic for general messages
const char *topic2 = "Button"; // MQTT topic for boot button
const int mqtt_port = 1883; // Standard MQTT port

// Define boot button pin (GPIO9)
const int bootButton = 9; // Boot button connected to GPIO9
bool buttonPressed = false; // Variable to store button state

// Objects for WLAN and MQTT communication
WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    Serial.begin(115200); // Start serial communication (baud rate: 115200)

    // Configure GPIO9 as input with internal pull-up resistor
    pinMode(bootButton, INPUT_PULLUP);

    // Establish connection to WLAN
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { // Wait as long as not connected
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to Wi-Fi"); // Report successful connection

    // Establish connection to MQTT broker
    client.setServer(mqtt_broker, mqtt_port);
    while (!client.connected()) {
        String client_id = "esp32-client-" + String(WiFi.macAddress()); // Create unique client ID
        Serial.printf("Connecting to MQTT Broker as %s\n", client_id.c_str());

        if (client.connect(client_id.c_str())) { // Attempt to connect
            Serial.println("Connected to MQTT Broker");
        } else {
            Serial.print("Connection failed: ");
            Serial.println(client.state()); // Output error code
            delay(2000); // Wait and try again
        }
    }

    // Send initial message to MQTT broker
    client.publish(topic, "ESP Client verbunden");
}

void loop() {
    // Maintain MQTT connection
    client.loop();

    // Read boot button state
    if (digitalRead(bootButton) == LOW) { // Button is pressed (LOW due to pull-up resistor)
        if (!buttonPressed) { // Ensure message is sent only once
            buttonPressed = true;
            Serial.println("Boot button pressed! Sending new message...");
            // Send message via MQTT broker
            client.publish(topic2, "Button pressed");
            delay(500); // Brief delay to eliminate bounce
        }
    } else {
        buttonPressed = false; // Reset state when button is released
    }
}