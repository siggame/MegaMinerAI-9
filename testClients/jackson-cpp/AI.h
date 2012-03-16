#ifndef AI_H
#define AI_H

#include "BaseAI.h"

#include <vector>

using namespace std;

///The class implementing gameplay logic.
class AI: public BaseAI
{
public:
  AI(Connection* c);
  virtual const char* username();
  virtual const char* password();
  virtual void init();
  virtual bool run();
  virtual void end();
  void warp();
  double shipValue(int i, vector<double> coreValue, vector< ShipType > deployment);
private:
  vector<Ship> m_myships;
  vector<Ship> m_enemyships;
  Ship m_mywarp;
  Ship m_enemywarp;
  int me;
};

#endif
