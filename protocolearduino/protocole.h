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

class Protocole {
	public:
    unsigned long MAX_TIME_TO_RECEIVE_A_BYTE = 100; //in milliseconds
		bool is_started = false;
    bool data_initialized = false;
    bool speed_of_iter_initialized = false;
    bool pos_0_initialized = false;
    bool memory_initialized = false;
    uint32_t memory = 5;
		uint32_t speed_of_iter;
		int32_t pos_0[8];
		uint32_t pos_in_data;
		int32_t **data;
		void init();
		void receive_speed_of_iter();
		void receive_pos_0();
		void receive_data();
    void send_memory();
    void ask_feed();
		void stop_motors();
		void start_motors();
    void send_ack();
    void receive_error();
		void send_error();
		void one_step_motors();
		bool is_initialized();
};
