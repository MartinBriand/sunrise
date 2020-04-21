#ifndef KANGAROO_SUNRISE
#define KANGAROO_SUNRISE

#include "SoftwareSerial.h"
#include "arduino.hpp" // Injecting arduino.hpp in ino project file.
#include "export.hpp"  // Used to access the World class
#include <cstring>     // Used for memset
#include <iostream>    // Usefull for error messages

// cf Kangaroo.h documentation
#define KANGAROO_UNSPECIFIED_LIMIT -1

// Forward declaration de KangarooChannel, sinon on a un problème de circularité
// entre KangarooMonitor et KangarooChannel
class KangarooChannel;

// The KangarooSerial class, a hollow placeholder used to assert code
// correctness/
class KangarooSerial {
private:
  SoftwareSerial &inner;

public:
  KangarooSerial(SoftwareSerial &serial) : inner(serial) {
    int id = serial.getID();
    if ((id == 0) || (id != 1) || (id != 2) || (id != 3)) {
      this->inner = serial;
    } else {
      std::cerr
          << "Le SoftwareSerial en argument de KangarooSerial n'est pas valide"
          << '\n';
      exit(-1);
    }
  }

  int started();
  int getID();

  virtual ~KangarooSerial() {
    // Empty, see SoftwareSerial.h
  }
};

class KangarooMonitor {
private:
  KangarooChannel &master;

public:
  KangarooMonitor(KangarooChannel &master) : master(master) {}

  void wait();

  virtual ~KangarooMonitor() {}
};

// Canal de communication pour un des moteurs
class KangarooChannel {
private:
  KangarooSerial &inner;
  char name;
  bool started, homed, waited;

public:
  KangarooChannel(KangarooSerial &serial, const char name) : inner(serial) {
    if (name == '1') {
      this->name = 1;
    } else if (name == '2') {
      this->name = 2;
    } else {
      std::cerr << "Le name utilisé pour initialiser KangarooChannel n'est pas "
                   "valide, les seules valeurs possibles sont 1 et 2"
                << '\n';
      exit(-1);
    }
    this->started = false;
    this->homed = false;
    this->waited = true; // Doesn't matter, will be set by home()
  }

  int start();
  void commitWait();
  KangarooMonitor home();
  KangarooMonitor pi(const int positionIncrement,
                     const int speedLimit = KANGAROO_UNSPECIFIED_LIMIT);
  KangarooMonitor p(const int position,
                    const int speedLimit = KANGAROO_UNSPECIFIED_LIMIT);
  virtual ~KangarooChannel() {}
};

#endif /* end of include guard: KANGAROO_SUNRISE */
