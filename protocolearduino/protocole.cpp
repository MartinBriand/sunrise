#include "protocole.h"

uint32_t receiveUint32_t () {

}

void sendUint32_t (uint32_t i) {
	uint8_t buf[4];
	//il faut tester si pas dans l'autre sens

}

void Protocole::init() {
	//ici on veut initilaliser toutes les variables une à une en début de communication

}

void Protocole::receive_speed() {
	//ici on reçoit la vitesse

}

void Protocole::receive_pos_0() {

}

void Protocole::receive_data() {

}

void Protocole::stop_motors() {

}

void Protocole::start_motors() {

}

void Protocole::send_error() {

}

void Protocole::one_step_motors() {

}





// uint16_t inByte;
//   uint8_t lengthOfVector = 3;
//   uint16_t vector[lengthOfVector];
//   uint8_t compteur = 0;
//   uint16_t res = 0;
  
//   uint8_t sendUInt16_t[2];


//   while (compteur < lengthOfVector) {
//     if (Serial.available()>=2) {
//       inByte = Serial.read()*256+Serial.read();
//       vector[compteur] = inByte; // read the incoming data   
//       compteur++;
//     }
//   }

//   if (compteur == lengthOfVector) {
//     for (int k = 0; k < lengthOfVector; k++) {
//       res+=vector[k];
//     }
//     uint16_tToBuf(res, sendUInt16_t);
//   }


  
