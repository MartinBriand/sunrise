#include "protocole.h"

// for this see this page -> https://www.tutorialspoint.com/cplusplus/cpp_this_pointer.htm
//test function
void blink_n_times(int n) {
  for (int k = 0; k < n ; k++) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(100);                       // wait for a second
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
    delay(100);
  }
}


//general functions
void reset_Protocole (Protocole *p) {
  while (Serial.available()) {
    Serial.read();
  }
  p->is_started = false;
  p->data_initialized = false;
  p->speed_of_iter_initialized = false;
  p->pos_0_initialized = false;
  p->memory_initialized = false;
}

void send_uint32_t(uint32_t a, Protocole *p) { //be careful, reading small digits first
  uint32_t acopy = a;
  uint8_t buf[4];
  for (int i = 0; i<4; i++) {
    buf[i] = acopy%256;
    acopy = acopy/256;
  }
  Serial.write(buf, 4);
}

bool receive_byte(uint8_t *i, Protocole *p) { //read one byte from stream
  Chrono chrono;
  chrono.restart();
  while ( chrono.elapsed() < p->MAX_TIME_TO_RECEIVE_A_BYTE) {
    if (Serial.available()){
      *i = Serial.read();
      return true;
    }
  }
  p->send_error(ERRORARDCODE::BYTE_TIMEOUT);
  return false;
}

bool receive_uint32_t(uint32_t *i, Protocole *p) { //reading big digits first
  uint32_t a = 0;
  uint8_t my_byte;
  for(int i = 0; i<4; i++) {
    a*=256;
    if (!receive_byte(&my_byte, p)) {return false;}
    a+=my_byte;
  }
  *i = a;
  return true;
}

bool receive_int32_t(int32_t *i, Protocole *p) {
  uint32_t my_uint32_t;
  bool res = receive_uint32_t(&my_uint32_t, p);
  if (res) {*i = my_uint32_t-2147483648;}
  return res;
}

bool receive_vector_of_8_int32_t (int32_t vector[], Protocole *p) {
  for (int i = 0; i<8; i++) {
    if (!receive_int32_t(&vector[i], p)) {return false;};
  }
  return true;
}


//protocole functions
bool Protocole::is_initialized () {
  return (this->data_initialized && this->speed_of_iter_initialized && this->pos_0_initialized && this->memory_initialized); 
}

bool Protocole::is_initialized_but_no_data () {
  return (!this->data_initialized && this->speed_of_iter_initialized && this->pos_0_initialized && this->memory_initialized);
}

bool Protocole::init() {
  //initialize
  this->is_started = false;
  this->data_initialized = false;
  this->speed_of_iter_initialized = false;
  this->pos_0_initialized = false;
  this->memory_initialized = false;
  //ack
  this->send_ack();
  return true;
}

bool Protocole::receive_speed_of_iter() {
  //first ack
  this->send_ack();
  //receive
  bool res = receive_uint32_t (&this->speed_of_iter, this);
  //ack
  if (res) {
    this->speed_of_iter_initialized = true;
    send_uint32_t(this->speed_of_iter, this);
  }
  return res;
}

bool Protocole::receive_pos_0() {
  // first ack
  this->send_ack();
  //receive
  bool res = receive_vector_of_8_int32_t(this->pos_0, this);
  // second ack
  if (res) {
    this->pos_0_initialized = true;
    this->send_ack();
  }
  return res;
}

bool Protocole::send_memory() {
  //send
  
  send_uint32_t(this->memory, this);
  
  //check
  uint32_t check;
  bool res = receive_uint32_t(&check, this);
  if (res && check == this->memory) {
    //ack
    this->memory_initialized = true;
    this->send_ack();
    return true;
  } else if (res) {//no need to raise error when res is false because error already raised before
    //error
    this->send_error(ERRORARDCODE::RECEIVED_WRONG_MEMORY);
    return false;
  }
}

bool Protocole::ask_feed() {
  Serial.write(CODEARD::FEED);
  uint8_t a;
  bool res = receive_byte(&a, this);
  if (res && a == CODEPY::DATA) {
    return this->receive_data();
  } else if (a == CODEPY::STOP) {
    this->receive_stop();
  } else {
    this->send_error(ERRORARDCODE::ASK_FEED_BAD_ANSWER);
  }
  return false;
}

bool Protocole::receive_data() {
  //ack
  this->send_ack();
  //init
  this->data = new int32_t *[this->memory];
  for (int i = 0 ; i < this->memory; i++) {
    this->data[i] = new int32_t[8];
  }
  //receive
  for(int i = 0 ; i < this->memory; i++) {
    if (!receive_vector_of_8_int32_t(this->data[i], this)) {
      return false;
    }
  }
  //ack
  this->send_ack();
  this->pos_in_data = 0;
  this->data_initialized = true;
  return true;
  }

bool Protocole::receive_stop() {
  this->is_started = false;
  this->send_ack();
  return true;
}

bool Protocole::receive_start() {
  if (this->is_initialized()) {
    this->is_started = true;
    this->send_ack();
    return true;
  } else if (this->is_initialized_but_no_data()){
    this->is_started = this->ask_feed();
    this->send_ack();
    return this->is_started;
  } else {
    this->send_error(ERRORARDCODE::START_WITHOUT_INITIALIZATION);
    return false;
  }
}

bool Protocole::send_ack() {
  Serial.write(CODEARD::ACK);
  return true;
}

bool Protocole::receive_error() {
  reset_Protocole(this);
  return true;
}

bool Protocole::send_error(ERRORARDCODE e) {
  Serial.write(CODEARD::ERRORARD);
  Serial.write(e);
  reset_Protocole(this);
  return true;
}



bool Protocole::one_step_motors() {
  //Cette fonction doit: faire tourner les moteurs d'un pas en vérifiant que l'écecution se fait bien dans les temps donnés pas la vitesse
  //Elle doit ensuite incrémenter le pointeur. si les données sont complètes, faire appelle à feed
  if (this->pos_in_data >= this->memory) {
    this->data_initialized = false;
    this->ask_feed();
    return false;
  } else {
    for(int k = 0; k<8; k++) {
      blink_n_times(this->data[this->pos_in_data][k]);
      delay(200);
    }
    delay(1000);
    this->pos_in_data += 1;
    return true;
  }
}
  
