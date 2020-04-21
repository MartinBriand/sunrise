#include "arduino.hpp"

int main(int argc, const char *argv[]) {
  SerialClass Serial = SerialClass();
  printf("%s\n", "Beginning connection");
  int code = Serial.begin(9600);
  printf("Code %d\n", code);
  printf("%s\n", "Connection established");
  Serial.println("Hello, World!");
  delay(1000);
  char buf[2];
  // Termination byte
  buf[1] = 0;
  size_t compt = 0;
  while (Serial.available()) {
    buf[0] = Serial.read();
    Serial.print(buf);
    printf("%ld\n", ++compt);
  }
  printf("%s\n", "End of connection");
  return 0;
}
