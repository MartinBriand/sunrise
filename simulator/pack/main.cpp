/*
The main used by the simulator when compiling the arduino source code.
*/
#include "arduino.hpp"
#include "export.hpp"
// Both needed to define the world class
#include "Kangaroo.h"
#include "SoftwareSerial.h"

int main(int argc, char const *argv[]) {
  signal(SIGINT, interruption);
  printf("%s\n%s\n", "Fichier de sortie : outfile.csv", "Port TCP : 1783");
  setup();

  // To avoid instantly creating a huge outfile.csv file.
  while (true) {
    loop();
    // Delay is used to avoid instantly flooding the outfile with garbage.
    delay(50);
    ZaWarudo.commit();
  }
  return 0;
}

int World::commit() {
  for (size_t i = 0; i < 9; i++) {
    this->outfile << this->current[i] << ';';
  }
  this->outfile << '\n';
  return 0;
}

void World::flush() { this->outfile.close(); }

void World::set(const int channel, const char name, const int position) {
  this->current[2 * channel + name] = position;
}

int World::get(const int channel, const char name) {
  return this->current[2 * channel + name];
}

void World::move(const int channel, const char name,
                 const int positionIncrement) {
  this->current[2 * channel + name] += positionIncrement;
}

void World::time(const int duration) { this->current[0] += duration; }

void interruption(int s) {
  std::cerr << '\n' << "---X Interruption" << '\n';
  ZaWarudo.flush(); // Write output to outfile.csv
  Serial.end();
  exit(1);
}
