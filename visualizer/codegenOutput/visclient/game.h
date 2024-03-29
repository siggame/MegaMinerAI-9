//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef GAME_H
#define GAME_H

#include "network.h"
#include "vc_structures.h"

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

namespace client
{

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

  _ShipType* ShipTypes;
  int ShipTypeCount;
  _Player* Players;
  int PlayerCount;
  _Ship* Ships;
  int ShipCount;
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

  ///Sends in a new ship of this type. Ships must be warped in with the radius of the player's warp ship.
  DLLEXPORT int shipTypeWarpIn(_ShipType* object, int x, int y);
  ///Allows a player to display messages on the screen
  DLLEXPORT int playerTalk(_Player* object, char* message);
  ///Command a ship to move to a specified position. If the position specified by this function is not legal, the position of the ship will be updated, but the movement will be rejected by the server.
  DLLEXPORT int shipMove(_Ship* object, int x, int y);
  ///Blow yourself up, damage those around you, reduces the ship to 0 health.
  DLLEXPORT int shipSelfDestruct(_Ship* object);
  ///Commands your ship to attack a target. Making an attack will reduce the number of attacks available to the ship, even if the attack is rejected by the game server.
  DLLEXPORT int shipAttack(_Ship* object, _Ship* target);

//derived properties



//accessors

DLLEXPORT int getTurnNumber(Connection* c);
DLLEXPORT int getPlayerID(Connection* c);
DLLEXPORT int getGameNumber(Connection* c);
DLLEXPORT int getRound(Connection* c);
DLLEXPORT int getVictoriesNeeded(Connection* c);
DLLEXPORT int getMapRadius(Connection* c);

DLLEXPORT _ShipType* getShipType(Connection* c, int num);
DLLEXPORT int getShipTypeCount(Connection* c);

DLLEXPORT _Player* getPlayer(Connection* c, int num);
DLLEXPORT int getPlayerCount(Connection* c);

DLLEXPORT _Ship* getShip(Connection* c, int num);
DLLEXPORT int getShipCount(Connection* c);



  DLLEXPORT int networkLoop(Connection* c);
#ifdef __cplusplus
}
#endif

}

#endif
