/*
Dummy library for the Arduino SoftwareSerial. Used only to force code
correctness.
*/

#ifndef SOFTWARE_SERIAL_SUNRISE
#define SOFTWARE_SERIAL_SUNRISE

// To do it the C++ way ...
#include "arduino.hpp" // Injecting arduino.hpp in ino project file.
#include <iostream>

class SoftwareSerial {
private:
  int id;
  bool start;

public:
  SoftwareSerial(const int id) {
    if ((id == 1) || (id == 2) || (id == 3)) {
      this->id = id;
    } else {
      std::cerr << "Il faut deux arguments pour déclarer un SoftwareSerial"
                << '\n';
      exit(-1);
    }
    this->start = false;
  }

  SoftwareSerial(const int rx, const int tx) {
    if (rx != 13) {
      std::cerr << "Le pin RX en argument de SoftwareSerial n'existe pas"
                << '\n';
      exit(-1);
    } else if (tx != 8) {
      std::cerr << "Le pin TX en argument de SoftwareSerial n'existe pas"
                << '\n';
      exit(-1);
    }
    this->id = 0;
    this->start = false;
  }

  void begin(const int baudrate) {
    int id = this->id;
    if ((id != 0) && (id != 1) && (id != 2) && (id != 3)) {
      std::cerr << "L'instance de SoftwareSerial sur laquelle vous avez appelé "
                   "begin n'est pas valide"
                << '\n';
      exit(-1);
    } else if (baudrate != 9600) {
      std::cerr << "L'argument baudrate passé à SoftwareSerial.begin n'est pas "
                   "valide, vous devez passer 9600"
                << '\n';
      exit(-1);
    }
    this->start = true;
  }

  int getID() { return this->id; }

  bool started() { return this->start; }

  virtual ~SoftwareSerial() {
    // The constructor must have a body or ld will throw a tantrum
  }
};

extern SoftwareSerial Serial1;
extern SoftwareSerial Serial2;
extern SoftwareSerial Serial3;

#endif /* end of include guard: SOFTWARE_SERIAL_SUNRISE */
