#ifndef LED_CONTROL_H
#define LED_CONTROL_H

#include <Arduino.h>

void led_control_init(uint8_t pin1, uint8_t pin2, uint8_t pin3, uint8_t pin4);
void led_on(uint8_t index);   // index: 1, 2, 3, 4
void led_off(uint8_t index);  // index: 1, 2, 3, 4
void led_all_on(void);
void led_all_off(void);

#endif // LED_CONTROL_H
