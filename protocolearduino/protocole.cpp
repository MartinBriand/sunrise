#include "protocole.h"

// for this see this page -> https://www.tutorialspoint.com/cplusplus/cpp_this_pointer.htm

//general functions
void send_uint32_t(uint32_t a, Protocole *p) { //be careful, reading small digits first
  uint32_t acopy = a;
  uint8_t* buf;
  for (int i = 0; i<4; i++) {
    buf[i] = acopy%256;
    acopy = acopy/256;
  }
  Serial.write(buf, 4);
}

uint8_t receive_byte(Protocole *p) { //read one byte from stream
  uint8_t a;
  Chrono chrono;
  chrono.restart();
  while ( chrono.elapsed() < p->MAX_TIME_TO_RECEIVE_A_BYTE) {
    if (Serial.available()){
      a = Serial.read();
      return a;
    }
  }
  p->send_error();
}

uint32_t receive_uint32_t(Protocole *p) { //reading big digits first
  uint32_t a = 0;
  for(int i = 0; i<4; i++) {
    a*=256;
    a+=receive_byte(p);
  }
  return a;
}

int32_t receive_int32_t(Protocole *p) {
  int64_t a = receive_uint32_t(p);
  int32_t b = a-2147483648;
  return b;
}

void receive_vector_of_8_int32_t (int32_t vector[], Protocole *p) {
  for (int i = 0; i<8; i++) {
    vector[i] = receive_int32_t(p);
  }
}


//protocole functions
bool Protocole::is_initialized () {
  return (this->data_initialized && this->speed_of_iter_initialized && this->pos_0_initialized && this->memory_initialized); 
}

void Protocole::init() {
  //initialize
  this->is_started = false;
  this->data_initialized = false;
  this->speed_of_iter_initialized = false;
  this->pos_0_initialized = false;
  this->memory_initialized = false;
  //ack
  this->send_ack();
}

void Protocole::receive_speed_of_iter() {
  //receive
  this->speed_of_iter = receive_uint32_t (this);
  //ack
  this->speed_of_iter_initialized = true;
  send_uint32_t(this->speed_of_iter, this);
}

void Protocole::receive_pos_0() {
  //receive
  receive_vector_of_8_int32_t(this->pos_0, this);
  //ack
  this->pos_0_initialized = true;
  this->send_ack();
}

void Protocole::send_memory() {
  //send
  send_uint32_t(this->max_number_of_instructions, this);
  //check
  uint32_t check = receive_uint32_t(this);
  if (check == this->max_number_of_instructions) {
    //ack
    this->memory_initialized = true;
    this->send_ack();
  } else {
    //error
    this->send_error();
  }
}

void Protocole::receive_data() {
  //receive
  this->data = new int32_t *[this->max_number_of_instructions];
  for (int i = 0 ; i < this->max_number_of_instructions; i++) {
    this->data[i] = new int32_t[8];
  }
  
  for(int i = 0 ; i < this->max_number_of_instructions; i++) {
    receive_vector_of_8_int32_t(this->data[i], this);
  }
  //ack
  this->send_ack();
}

void Protocole::receive_error() {
  this->init();
}

void Protocole::stop_motors() {
  this->is_started = false;
  this->send_ack();
}

void Protocole::start_motors() {
  if (this->is_initialized()) {
    this->is_started = true;
    this->send_ack();
  } else {
    this->send_error();
  }
}

void Protocole::send_error() {
  Serial.write(CODESEND::ERRORARD);
}

void Protocole::send_ack() {
  Serial.write(CODESEND::ACK);
}

void Protocole::one_step_motors() {
  //Cette fonction doit: faire tourner les moteurs d'un pas en vérifiant que l'écecution se fait bien dans les temps donnés pas la vitesse
  //Elle doit ensuite incrémenter le pointeur. si les données sont complètes, faire appelle à feed

}
  
