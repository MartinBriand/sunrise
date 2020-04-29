#include "protocole.h"
#include <stdint.h>
//Use stdint.h for a minimal set of definitions; use inttypes.h if you also need portable support for these in printf, scanf, et al.

uint8_t inByte;
Protocole p;

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() == 1) {
    inByte = Serial.read();
    switch (inByte) {
      case CODEPY::INITIAL :
        p.init();
        break;
      case CODEPY::SPEED :
        p.receive_speed_of_iter();
        break;
      case CODEPY::POS_0 :
        p.receive_pos_0();
        break;
      case CODEPY::MEMORY :

        p.send_memory();
        break;
      case CODEPY::DATA :
        p.receive_data();
        break;
      case CODEPY::STOP :
        p.receive_stop();
        break;
      case CODEPY::START :
        p.receive_start();
        break;
      case CODEPY::ERRORPY :
        p.receive_error();
        break;
      default :
        p.send_error();
    }
  } else if (Serial.available() > 1) {
    p.send_error();
  } else if (p.is_started) {
    p.one_step_motors();
  }
}
