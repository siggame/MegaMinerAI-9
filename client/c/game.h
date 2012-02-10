//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)

#ifdef ENABLE_THREADS
#include "pthread.h"
#endif

#else
#define DLLEXPORT

#ifdef ENABLE_THREADS
#include <pthread.h>
#endif

#endif

struct Connection
{
  int socket;
  
  #ifdef ENABLE_THREADS
  pthread_mutex_t mutex;
  #endif
  
  int turnNumber;
  int playerID;
  int gameNumber;
  int round;
  int victoriesNeeded;
  int mapRadius;

  _Player* Players;
  int PlayerCount;
  _Ship* Ships;
  int ShipCount;
  _ShipType* ShipTypes;
  int ShipTypeCount;
};

#ifdef __cplusplus
extern "C"
{
#endif
  DLLEXPORT Connection* createConnection();
  DLLEXPORT void destroyConnection(Connection* c);
  DLLEXPORT int serverConnect(Connection* c, const char* host, const char* port);

  DLLEXPORT int serverLogin(Connection* c, const char* username, const char* password);
  DLLEXPORT int createGame(Connection* c);
  DLLEXPORT int joinGame(Connection* c, int id, const char* playerType);

  DLLEXPORT void endTurn(Connection* c);
  DLLEXPORT void getStatus(Connection* c);


//commands

  ///
  DLLEXPORT int playerTalk(_Player* object, char* message);
  ///
  DLLEXPORT int shipMove(_Ship* object, int x, int y);
  ///
  DLLEXPORT int shipSelfDestruct(_Ship* object);
  ///
  DLLEXPORT int shipAttack(_Ship* object, _Ship* target);
  ///
  DLLEXPORT int shiptypeWarpIn(_ShipType* object, int x, int y);

//derived properties



//accessors

DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getPlayerID(Connection* c);
DLLEXPORT int getGameNumber(Connection* c);
DLLEXPORT int getRound(Connection* c);
DLLEXPORT int getVictoriesNeeded(Connection* c);
DLLEXPORT int getMapRadius(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);

DLLEXPORT _Ship* getShip(Connection* c, int num);
DLLEXPORT int getShipCount(Connection* c);

DLLEXPORT _ShipType* getShipType(Connection* c, int num);
DLLEXPORT int getShipTypeCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

#endif
