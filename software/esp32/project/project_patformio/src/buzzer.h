#ifndef BUZZER_H
#define BUZZER_H

#include <Arduino.h>



	void buzzer_init(uint8_t pin);
	void buzzer_on(void);
	void buzzer_off(void);
	void buzzer_beep(uint16_t duration_ms); 



#endif // BUZZER_H
