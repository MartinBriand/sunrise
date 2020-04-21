#include "protocole.h"
// for this see this page -> https://www.tutorialspoint.com/cplusplus/cpp_this_pointer.htm


void sendUint32_t(uint32_t a) { //be careful, reading small digits first
  uint32_t acopy = a;
  uint8_t* buf;
  for (int i = 0; i<4; i++) {
    buf[i] = acopy%256;
    acopy = acopy/256;
  }
  Serial.write(buf, 4);
}

uint32_t receiveUint32_t() {
  uint32_t a = 0;
  for(int i = 0; i<4; i++) {
    a*=256;
    a+=Serial.read();
  }
  return a;
}

bool Protocole::is_initialized () {
  return (this->data_initialized && this->speed_of_iter_initialized && this->pos_0_initialized); 
}

void Protocole::init() {
  isStarted = false;
  data_initialized = false;
  speed_of_iter_initialized = false;
  pos_0_initialized = false;
}

void Protocole::receive_speed() {

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
  //Cette fonction doit: faire tourner les moteurs d'un pas en vérifiant que l'écecution se fait bien dans les temps donnés pas la vitesse
  //Elle doit ensuite incrémenter le pointeur. si les données sont complètes, faire appelle à feed

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


  
