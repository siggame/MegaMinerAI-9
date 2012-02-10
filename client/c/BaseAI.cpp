//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that

#include "BaseAI.h"
#include "game.h"

int BaseAI::turnNumber()
{
  return getTurnNumber(c);
}
int BaseAI::playerID()
{
  return getPlayerID(c);
}
int BaseAI::gameNumber()
{
  return getGameNumber(c);
}
int BaseAI::round()
{
  return getRound(c);
}
int BaseAI::victoriesNeeded()
{
  return getVictoriesNeeded(c);
}
int BaseAI::mapRadius()
{
  return getMapRadius(c);
}

bool BaseAI::startTurn()
{
  static bool initialized = false;
  int count = 0;
  count = getPlayerCount(c);
  players.clear();
  players.resize(count);
  for(int i = 0; i < count; i++)
  {
    players[i] = Player(getPlayer(c, i));
  }

  count = getShipCount(c);
  ships.clear();
  ships.resize(count);
  for(int i = 0; i < count; i++)
  {
    ships[i] = Ship(getShip(c, i));
  }

  count = getShipTypeCount(c);
  shipTypes.clear();
  shipTypes.resize(count);
  for(int i = 0; i < count; i++)
  {
    shipTypes[i] = ShipType(getShipType(c, i));
  }

  if(!initialized)
  {
    initialized = true;
    init();
  }
  return run();
}

BaseAI::BaseAI(Connection* conn) : c(conn) {}
BaseAI::~BaseAI() {}
