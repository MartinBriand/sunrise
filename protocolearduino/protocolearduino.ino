#include "protocole.h"
#include <stdint.h>
//Use stdint.h for a minimal set of definitions; use inttypes.h if you also need portable support for these in printf, scanf, et al.

uint8_t inByte;
Protocole p;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() == 1) {
    inByte = Serial.read();
    switch (inByte) {
      case CODERECEIVE::INITIAL :
        p.init();
        break;
      case CODERECEIVE::SPEED :
        p.receive_speed_of_iter();
        break;
      case CODERECEIVE::POS_0 :
        p.receive_pos_0();
        break;
      case CODERECEIVE::MEMORY :
        p.send_memory();
        break;
      case CODERECEIVE::DATA :
        p.receive_data();
        break;
      case CODERECEIVE::STOP :
        p.stop_motors();
        break;
      case CODERECEIVE::START :
        p.start_motors();
        break;
      case CODERECEIVE::ERRORPY :
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
