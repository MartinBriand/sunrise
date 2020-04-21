// Movement Sample for Kangaroo
// Copyright (c) 2013 Dimension Engineering LLC
// See license.txt for license details.

#include "Kangaroo.h"
#include "SoftwareSerial.h"

// Arduino TX (pin 1/18/16/14) goes to Kangaroo S1
// Arduino RX (pin 0/19/17/15) goes to Kangaroo S2
// Arduino GND                 goes to Kangaroo 0V
// Arduino 5V                  goes to Kangaroo 5V (OPTIONAL, if you want
// Kangaroo to power the Arduino)
#define TXK_PIN 8
#define RXK_PIN 13

// Si échec de téléversement, débrancher les ports 1 et 0 (TX0 / RX0).

int cursor = 0; // Note : index is already reserved by string.h
int coords[4];
int pos_ini[] = {0, 0, 0, 0};
int speed = 102;
int tour = 256;
int byte_read = 0;  ///< The current byte read.
int separator = 32; ///< The separator between the integers (44=, and 32=Space)

// Independent mode channels on Kangaroo are, by default, '1' and '2'.
// on crée une instance d'un objet SoftwareSerial. RXK_PIN reçoit les data en
// série, TXK_PIN transmet les data en série
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

void setup() {
  // définir la vitesse pour la communication en série
  Serial.begin(9600);
  SerialPortK.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);

  // starts the channels, homes the channels, waits until the complete execution
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
  // increment the position
  K1.p(0).wait();
  L1.p(0).wait();
  M1.p(0).wait();
  N1.p(0).wait();
  Serial.println("pret");
}

// deux fonctions qui permettent de lire les nombres avec l'arduino
boolean is_a_number(int n) { return n >= 48 && n <= 57; }

int ascii2int(int n, int byte_read) { return n * 10 + (byte_read - 48); }

// .wait() waits until the command is 'finished'. For position, this means it is
// within the deadband distance from the requested position. You can also call
// K1.p(position); without .wait() if you want to command it but not wait until
// it gets to the destination. If you do this, you may want to use
// K1.getP().value() to check progress. Dérouler : > 0 Enrouler : < 0
void loop() {
  cursor = 0; ///< 0: reading x, 1: reading y.

  coords[0] = 0;
  coords[1] = 0;
  coords[2] = 0;
  coords[3] = 0;
  bool neg = false;
  while (Serial.available() > 0) {
    // on lit l'incrément de position souhaité par l'utilisateur
    byte_read = Serial.read();
    // neg est vrai si on met un signe négatif dans le byte-read
    neg = (byte_read == 45 || neg == true);
    // Serial.println(byte_read);
    // on vérifie que  c'est bien un nombre
    if (is_a_number(byte_read)) {
      // on associe au moteur n°index la coordonnée entrée par l'utilisateur
      coords[cursor] = ascii2int(coords[cursor], byte_read);
    }
    // si on arrive à une fin de ligne ou à une virgule, on incrémente index de
    // 1 et on passa au moteur suivant
    else if (byte_read == separator || byte_read == 10) {
      // on met la coordonnée en négatif si l'utilisateur a écrit un signe -
      if (neg) {
        coords[cursor] = -coords[cursor];
        neg = false;
      }
      // on incrémente l'index pour passer au moteur suivant
      ++cursor;
    }
  }

  if (cursor) {
    // Go to the commanded positions at the defined speed.
    // on écrit les incréments de positions souhaités
    Serial.print("I = ");
    Serial.println(coords[0] - pos_ini[0]);
    Serial.print("II = ");
    Serial.println(coords[1] - pos_ini[1]);
    Serial.print("III = ");
    Serial.println(coords[2] - pos_ini[2]);
    Serial.print("IV = ");
    Serial.println(coords[3] - pos_ini[3]);
    // on redéfinit la position que doit avoir le moteur
    K1.p(coords[0] - pos_ini[0], speed).wait();
    L1.p(coords[1] - pos_ini[1], speed).wait();
    M1.p(coords[2] - pos_ini[2], speed).wait();
    N1.p(coords[3] - pos_ini[3], speed).wait();
    // on envoie la commande au moteur pour aller à la position voulue
    K1.pi(coords[0], speed).wait();
    L1.pi(coords[1], speed).wait();
    M1.pi(coords[2], speed).wait();
    N1.pi(coords[3], speed).wait();
  } else {
    // Serial.println();
  }

  delay(1000);
}

void readData() { Serial; }
