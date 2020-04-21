/*
Header used to reexport the arduino project file into C++ code and inject it in
a main.
*/

#ifndef EXPORTED_SUNRISE
#define EXPORTED_SUNRISE

#include <fstream>  // Used to write the positions to outfile.csv
#include <signal.h> // Used to handle Ctrl-C correctly

typedef bool boolean; // bool is arduino's name for c++ boolean

class World {
  // WRRRRRRRRYYYYYYYYYY !!!!!!!!
private:
  std::ofstream outfile;
  int current[9]; // This is intentionaly not initialized at the beginning of
                  // the execution.

public:
  World() {
    this->current[0] = 0; // The first value represents time.
    this->outfile.open("outfile.csv");
  }

  void set(const int channel, const char name, const int position);
  int get(const int channel, const char name);
  void move(const int channel, const char name, const int positionIncrement);
  void time(const int duration);

  int commit(); // Appends changes to outfile.csv
  void
  flush(); // Used explicitely when the application is interrupted with Ctrl-C.

  virtual ~World() { this->outfile.close(); }
};

extern World ZaWarudo;

void setup();
void loop();
void interruption(int s); // Used to catch Ctrl-C interruption.

#endif /* end of include guard: EXPORTED_SUNRISE */
