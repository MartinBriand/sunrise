/*
This header file is part of the SunRise Arduino simulator meant to test the
correctness of our Arduino code without having physical access to our hardware.

The functionnalities reimplemented here are :
 - Simple Serial IO
 - delay

*/

#ifndef ARDUINO_SUNRISE
#define ARDUINO_SUNRISE

#include "export.hpp" // Needed to update world time with delay.
#include <chrono>     // Used to implement delay
#include <thread> // Mandatory because the emulator has to do some things in the background.

// The Linux API are written in C and there is not much I can do about that.
#include <arpa/inet.h>  // Required for htonl in tcp communication
#include <cstdlib>      // Required for tcp communication
#include <cstring>      // Because legacy calls for legacy
#include <sys/socket.h> // Required for tcp communication
#include <unistd.h>     // Required for tcp communication

#define PORT 1783

class SerialClass {
private:
  // Used for TCP communication
  int sockfd;
  int connfd;
  struct sockaddr_in server;
  struct sockaddr_in client;

public:
  /*
  Initializing POD that will be used with a C API is kind of pointless, hence
  the empty constructor.
  */
  SerialClass() {}
  // Note that baudrate is ignored in this implementation.
  int begin(int baudrate);
  // Defined in arduino and usefull in case of Ctrl-C
  void end();
  int available();
  int read();
  int readBytes(char *buffer, int length);
  size_t print(const char *msg);
  size_t print(int msg);
  size_t println();
  size_t println(const char *msg);
  size_t println(int msg);
  virtual ~SerialClass() {
    // Not sure whether this ever gets called.
    close(this->sockfd);
  }
};

void delay(int duration);

extern SerialClass Serial;

#endif /* end of include guard: ARDUINO_SUNRISE */
