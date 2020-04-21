/*
Simple test to see whether the implementation of the Kangaroo library can be
substituted successfully.
*/
#include "Kangaroo.h"
#include "SoftwareSerial.h"

#define TXK_PIN 8
#define RXK_PIN 13
#define TOUR 256

SoftwareSerial SerialPortK(RXK_PIN, TXK_PIN); // Devant droite
KangarooSerial K(SerialPortK);
KangarooChannel K1(K, '1');
KangarooChannel K2(K, '2');
KangarooSerial L(Serial1); // Derrière droite
KangarooChannel L1(L, '1');
KangarooChannel L2(L, '2');
KangarooSerial M(Serial2);
KangarooChannel M1(M, '1');
KangarooChannel M2(M, '2');
KangarooSerial N(Serial3);
KangarooChannel N1(N, '1');
KangarooChannel N2(N, '2');

int main(int argc, char const *argv[]) {
  SerialPortK.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);

  K1.start();
  K1.home().wait();
  K2.start();
  K2.home().wait();
  L1.start();
  L1.home().wait();
  L2.start();
  L2.home().wait();
  M1.start();
  M1.home().wait();
  M2.start();
  M2.home().wait();
  N1.start();
  N1.home().wait();
  N2.start();
  N2.home().wait();

  for (size_t i = 0; i < 8; i++) {
    ZaWarudo.commit();
    K1.pi(3 * TOUR).wait();
    L1.pi(3 * TOUR).wait();
    M1.pi(3 * TOUR).wait();
    N1.pi(3 * TOUR).wait();
  }

  return 0;
}
