#include "AI.h"
#include "util.h"
#include <math.h>
#include <stdlib.h>

#define PI 3.1415

AI::AI(Connection* conn) : BaseAI(conn) {}

const char* AI::username()
{
  return "Shell AI";
}

const char* AI::password()
{
  return "password";
}

//This function is run once, before your first turn.
void AI::init()
{
}

double AI::shipValue(int s, vector<double> coreValue, vector< ShipType > deployment)
{
  vector<double> value;
  for(int i=0; i < deployment.size(); i++)
  {
    int j;
    for(j=0; j < shipTypes.size() && deployment[i].id() != shipTypes[j].id(); j++);
    coreValue[j]--;
    if(coreValue[j] < 1)
    {
      coreValue[j] = 1;
    } 
  }
  return coreValue[s];
}

void AI::warp()
{
  typedef pair<double, vector< ShipType > > kitem;
  vector< kitem > m;
  m.resize(players[playerID()].energy()+1);
  m[0] = kitem(0.0, vector< ShipType >());
  vector<double> coreValue;
  for(int i = 0; i < shipTypes.size(); i++)
  {
    coreValue.push_back(shipTypes[i].cost() * 1.0);
  }
  for(int i = 1; i < m.size(); i++)
  {
    double bestv = m[i-1].first;
    vector< ShipType > bests = m[i-1].second;
    for(int j = 0; j < shipTypes.size(); j++)
    {
      if(shipTypes[j].cost() > i)
      {
        continue;
      }
      vector< ShipType > news = m[i-shipTypes[j].cost()].second;
      double newv = shipValue(j,coreValue,news)+ m[i-shipTypes[j].cost()].first;
      if(newv > bestv)
      {
        bestv = newv;
        bests = news;
      }
    }
  }
  for(int i=0; i < m[m.size()-1].second.size(); i++) 
  {
    m[m.size()-1].second[i].warpIn(m_mywarp.x(),m_mywarp.y());
  }
}

//This function is called each time it is your turn.
//Return true to end your turn, return false to ask the server for updated information.
bool AI::run()
{
  for(int i=0; i < ships.size(); i++)
  {
    if(ships[i].owner() == playerID())
    {
      m_myships.push_back(ships[i]);
    }
    else
    {
      m_enemyships.push_back(ships[i]);
    }
  }
  warp();
  for(int i=0; i < m_myships.size(); i++)
  {
    int r = m_myships[i].movementLeft();
    int d = random() % 360;
    int x = r*cos((d*PI)/180);
    int y = r*sin((d*PI)/180);
    m_myships[i].move(m_myships[i].x()+x,m_myships[i].y()+y);
  }
  return true;
}

//This function is run once, after your last turn.
void AI::end(){}
