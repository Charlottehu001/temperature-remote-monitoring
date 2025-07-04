#include "buzzer.h"

static uint8_t buzzer_pin = 0;

void buzzer_init(uint8_t pin)
{
	buzzer_pin = pin;
	pinMode(buzzer_pin, OUTPUT);
	digitalWrite(buzzer_pin, LOW); 
}

void buzzer_on(void)
{
	digitalWrite(buzzer_pin, HIGH);
}

void buzzer_off(void)
{
	digitalWrite(buzzer_pin, LOW);
}

void buzzer_beep(uint16_t duration_ms)
{
	buzzer_on();
	delay(duration_ms);
	buzzer_off();
}
