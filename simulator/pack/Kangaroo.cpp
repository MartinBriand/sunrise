/*
Dummy implementation of the Kangaroo.h library.
*/

#include "Kangaroo.h"

int KangarooSerial::started() { return this->inner.started(); }

int KangarooSerial::getID() { return this->inner.getID(); }

int KangarooChannel::start() {
  if (!inner.started()) {
    std::cerr << "Vous devez initier la liaison série avec begin avant de "
                 "d'utiliser le canal Kangaroo associé"
              << '\n';
    exit(-1);
  }
  this->started = true;
  return 0;
}

void KangarooChannel::commitWait() { this->waited = true; }

KangarooMonitor KangarooChannel::home() {
  if (!this->started) {
    std::cerr
        << "Vous devez démarrer le canal avec start avant de l'utiliser home"
        << '\n';
    exit(-1);
  }
  this->homed = true;
  this->waited = false;
  // Note that this return invokes a copy constructor
  return KangarooMonitor(*this);
}

// Default argument specified in header
KangarooMonitor KangarooChannel::p(const int position, const int speedLimit) {
  if (!this->started) {
    std::cerr << "Vous devez démarrer le canal avec start avant de l'utiliser "
                 "avec la méthode p"
              << '\n';
    exit(-1);
  }
  if (!this->started) {
    std::cerr << "Vous devez initialiser le canal avec home avant de "
                 "l'utiliser avec la méthode p"
              << '\n';
    exit(-1);
  }
  if (!this->waited) {
    std::cerr << "Vous n'avez pas attendu une action précédente sur ce canal, "
                 "qui est toujours considérée en cours"
              << '\n';
    exit(-1);
  }
  int old = ZaWarudo.get(this->inner.getID(), this->name);
  // Updating space in World
  ZaWarudo.set(this->inner.getID(), this->name, position);
  this->waited = false;
  // Updating time in World
  if (speedLimit == KANGAROO_UNSPECIFIED_LIMIT) {
    // Nothing to do here, I assume that the motor goes in place as fast as
    // possible.
  } else if (speedLimit <= 0) {
    std::cerr << "La limite de vitesse passée à la méthode pi doit être "
                 "strictement positive"
              << '\n';
    exit(-1);
  } else {
    if (old > position) {
      ZaWarudo.time((old - position) / speedLimit);
    } else {
      ZaWarudo.time((position - old) / speedLimit);
    }
  }
  return KangarooMonitor(*this);
}

// Default argument specified in header
KangarooMonitor KangarooChannel::pi(const int positionIncrement,
                                    const int speedLimit) {
  if (!this->started) {
    std::cerr << "Vous devez démarrer le canal avec start avant de l'utiliser "
                 "avec la méthode pi"
              << '\n';
    exit(-1);
  }
  if (!this->started) {
    std::cerr << "Vous devez initialiser le canal avec home avant de "
                 "l'utiliser avec la méthode pi"
              << '\n';
    exit(-1);
  }
  if (!this->waited) {
    std::cerr << "Vous n'avez pas attendu une action précédente sur ce canal, "
                 "qui est toujours considérée en cours"
              << '\n';
    exit(-1);
  }
  // Updating spatial coordonnates
  ZaWarudo.move(this->inner.getID(), this->name, positionIncrement);
  this->waited = false;
  // Updating temporal coordonnates
  if (speedLimit == KANGAROO_UNSPECIFIED_LIMIT) {
    // Nothing to do here, I assume that the motor goes in place as fast as
    // possible.
  } else if (speedLimit <= 0) {
    std::cerr << "La limite de vitesse passée à la méthode pi doit être "
                 "strictement positive"
              << '\n';
    exit(-1);
  } else {
    ZaWarudo.time(positionIncrement / speedLimit);
  }
  return KangarooMonitor(*this);
}

void KangarooMonitor::wait() { this->master.commitWait(); }
