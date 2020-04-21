#include <stdint.h>

enum CODESEND : uint8_t {
  memoire = 4,
  feed = 6,
  ack = 10,
  erreur = 11  
};

enum CODERECEIVE : uint8_t {
  initial = 2,
  vitesse = 3,
  pos_0 = 5,
  data = 7,
  stop = 8,
  start = 9
};

class Protocole {
	public:
		bool isInitialized = false;
		bool isStarted = false;
		uint32_t speed;
		uint32_t pos_0;
		uint32_t pos_in_data;
		int32_t data[][8];
		void init();
		void receive_speed();
		void receive_pos_0();
		void receive_data();
		void stop_motors();
		void start_motors();
		void send_error();
		void one_step_motors();
};