/*
Implementation of arduino.hpp, this file holds various functions such as :
 - delay
*/

#include "arduino.hpp"

void delay(int duration) {
  // Although what this code does is fairly obvious when you read it, I am going
  // to complain that "the C++" way is quite ugly.
  std::this_thread::sleep_for(std::chrono::milliseconds(duration));
  ZaWarudo.time(duration);
}
