#include <stdint.h>
#include "arduino.h"
#include <Chrono.h>

enum CODEARD : uint8_t {
  FEED = 6,
  ACK = 10,
  ERRORARD = 11,  
};

enum CODEPY : uint8_t {
  INITIAL = 2,
  SPEED = 3,
  MEMORY = 4,
  POS_0 = 5,
  DATA = 7,
  STOP = 8,
  START = 9,
  ERRORPY = 11,
};

enum ERRORARDCODE : uint8_t {//more than 20
  WRONG_INSTRUCTION = 20,
  TOO_MANY_INSTRUCTIONS = 21,
  START_WITHOUT_INITIALIZATION = 22,
  ASK_FEED_BAD_ANSWER = 23,
  RECEIVED_WRONG_MEMORY = 24,
  BYTE_TIMEOUT = 25,
  
};

class Protocole {
	public:
    unsigned long MAX_TIME_TO_RECEIVE_A_BYTE = 100; //in milliseconds
		bool is_started = false;
    bool data_initialized = false;
    bool speed_of_iter_initialized = false;
    bool pos_0_initialized = false;
    bool memory_initialized = false;
    uint32_t memory = 40; //this is the maximum for an arduino nano
		uint32_t speed_of_iter;
		int32_t pos_0[8];
		uint32_t pos_in_data;
		int32_t **data;
		bool init();
		bool receive_speed_of_iter();
		bool receive_pos_0();
		bool receive_data();
    bool send_memory();
    bool ask_feed();
		bool receive_stop();
		bool receive_start();
    bool send_ack();
    bool receive_error();
		bool send_error(ERRORARDCODE);
		bool one_step_motors();
		bool is_initialized();
    bool is_initialized_but_no_data();
};
