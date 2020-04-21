/*
Implementation of the arduino.hpp library. This file contains code related to
the Serial connection.
*/

#include "arduino.hpp"
#include <iostream> // Usefull for error messages

int SerialClass::begin(int baudrate) {
  // Note that this implementation was largely inspired by
  // https://www.geeksforgeeks.org/tcp-server-client-implementation-in-c/

  unsigned int len;

  // Step 1 : Request Socket from OS
  this->sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (this->sockfd == -1) {
    return -1;
  }
  // else ...

  // Setting server to zero
  memset(&(this->server), 0, sizeof(this->sockfd));

  // Step 2 : Preparing the bind
  this->server.sin_family = AF_INET;
  this->server.sin_addr.s_addr = htonl(INADDR_ANY);
  this->server.sin_port = htons(PORT);

  // Step 3 : Assigning a name to the socket
  if ((bind(this->sockfd, (struct sockaddr *)&(this->server),
            sizeof(this->server))) != 0) {
    std::cerr << "Une erreur réseau s'est produite : " << strerror(errno)
              << '\n';
    return -2;
  }
  // else ...

  // Step 4 : Listening for client
  if ((listen(this->sockfd, 1)) != 0) {
    return -3;
  }
  // else ...

  // Step 5 : Connecting the client
  len = (unsigned int)sizeof(
      this->client); // Type size_t would not work for accept()
  this->connfd = accept(sockfd, (struct sockaddr *)&(this->client), &len);
  if (this->connfd < 0) {
    return -4;
  }
  // else ...

  // Connection has been established correctly.
  return true;
}

int SerialClass::available() {
  // A buffer for recv, the size was chosen with the application in mind.
  char buffer[20];
  // Number of bytes available from the socket
  int returnValue =
      (int)recv(this->connfd, &buffer, sizeof(buffer), MSG_PEEK | MSG_DONTWAIT);
  if (returnValue > 0) { // i.e. there are some bytes to read
    return returnValue;
  } else { // early fail because there aren't any more bytes to read
    return 0;
  }
}

int SerialClass::read() {
  // Note : this API is extremely inefficient for a TCP connection. It returns
  // the next byte as an int.
  char buffer;
  ssize_t bytes = recv(this->connfd, &buffer, sizeof(buffer), 0);
  if (bytes >= 0) {
    return (int)buffer;
  } else {
    // cf Arduino documentation
    return -1;
  }
}

int SerialClass::readBytes(char *buffer, int length) {
  return (int)recv(this->connfd, buffer, length, 0);
}

void SerialClass::end() {
  close(this->sockfd);
  close(this->connfd);
}

size_t SerialClass::print(const char *msg) {
  // MSG_NOSIGNAL prevents send from killing the process in case of SIGPIPE
  ssize_t bytes = send(this->connfd, msg, strlen(msg), MSG_NOSIGNAL);
  if (bytes > 0) {
    return (size_t)bytes;
  } else {
    // Weird, Serial::print doesn't seem to have an error code in the
    // documentation.
    return false;
  }
}

size_t SerialClass::print(int msg) {
  char buffer[10];
  ssize_t bytes;
  int count = snprintf((char *)buffer, sizeof(buffer), "%d", msg);
  if (count > sizeof(buffer)) {
    // buffer was too small
    char *big = new char[count];
    snprintf(big, count, "%d", msg);
    bytes = send(this->connfd, big, count, MSG_NOSIGNAL);
    delete[] big;
  } else {
    // MSG_NOSIGNAL prevents send from killing the process in case of SIGPIPE
    bytes = send(this->connfd, &buffer, count, MSG_NOSIGNAL);
  }
  if (bytes > 0) {
    return (size_t)bytes;
  } else {
    // Weird, Serial::print doesn't seem to have an error code in the
    // documentation.
    return false;
  }
}

size_t SerialClass::println() {
  char buffer = '\n';
  // MSG_NOSIGNAL prevents send from killing the process in case of SIGPIPE
  ssize_t bytes = send(this->connfd, &buffer, sizeof(buffer), MSG_NOSIGNAL);
  if (bytes > 0) {
    return (size_t)bytes;
  } else {
    // Weird, Serial::print doesn't seem to have an error code in the
    // documentation.
    return false;
  }
}

size_t SerialClass::println(const char *msg) {
  size_t a = this->print(msg);
  size_t b = this->println();
  return a + b;
}

size_t SerialClass::println(int msg) {
  size_t a = this->print(msg);
  size_t b = this->println();
  return a + b;
}
