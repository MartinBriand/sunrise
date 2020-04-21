#include "SoftwareSerial.h"

#define TXK_PIN 8
#define RXK_PIN 13

int main(int argc, char const *argv[]) {
  SoftwareSerial SerialPortK(RXK_PIN, TXK_PIN); // Devant droite
  printf("%ld\n", sizeof(Serial1));
  printf("%ld\n", sizeof(Serial2));
  printf("%ld\n", sizeof(Serial3));
  return 0;
}
