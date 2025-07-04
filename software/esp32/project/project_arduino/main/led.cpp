#include "led.h"

#define LED_COUNT 4

static uint8_t led_pins[LED_COUNT];

void led_control_init(uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4)
{
    led_pins[0] = pin1;
    led_pins[1] = pin2;
    led_pins[2] = pin3;
    led_pins[3] = pin4;

    for (int i = 0; i < LED_COUNT; i++)
    {
        pinMode(led_pins[i], OUTPUT);
        digitalWrite(led_pins[i], LOW); // Default off
    }
}

void led_on(uint8_t index)
{
    if (index < LED_COUNT)
    {
        digitalWrite(led_pins[index], HIGH);
    }
}

void led_off(uint8_t index)
{
    if (index < LED_COUNT)
    {
        digitalWrite(led_pins[index], LOW);
    }
}

void led_all_on(void)
{
    for (int i = 0; i < LED_COUNT; i++)
    {
        digitalWrite(led_pins[i], HIGH);
    }
}

void led_all_off(void)
{
    for (int i = 0; i < LED_COUNT; i++)
    {
        digitalWrite(led_pins[i], LOW);
    }
}
