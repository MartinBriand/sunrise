#include "protocole.h"
#include <stdint.h>
//Use stdint.h for a minimal set of definitions; use inttypes.h if you also need portable support for these in printf, scanf, et al.

uint8_t inByte;
Protocole p;

void sendUint16_t(uint16_t a) {
  uint8_t* buf;
  buf[0] = a/256;
  buf[1] = a%256;
  Serial.write(buf, 2);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() == 1) {
    inByte = Serial.read();
    switch (inByte) {
      case CODERECEIVE::initial :
        p.init();
        break;
      case CODERECEIVE::vitesse :
        p.receive_speed();
        break;
      case CODERECEIVE::pos_0 :
        p.receive_pos_0();
        break;
      case CODERECEIVE::data :
        p.receive_data();
        break;
      case CODERECEIVE::stop :
        p.stop_motors();
        break;
      case CODERECEIVE::start :
        p.start_motors();
        break;
      default :
        p.send_error();
    }
  } else if (Serial.available() > 1) {
    p.send_error();
  } else if (p.isStarted) {
    p.one_step_motors();
  }
}
