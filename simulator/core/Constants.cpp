/*
This file defines various constants that exist in the arduino library and that
we need for the simulator.
*/

#include "Kangaroo.h"
#include "SoftwareSerial.h"
#include "arduino.hpp"

World ZaWarudo;

SoftwareSerial Serial1 = SoftwareSerial(1);
SoftwareSerial Serial2 = SoftwareSerial(2);
SoftwareSerial Serial3 = SoftwareSerial(3);

SerialClass Serial;
