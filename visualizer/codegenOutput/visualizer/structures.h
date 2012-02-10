//Copyright (C) 2009 - Missouri S&T ACM AI Team
//Please do not modify this file while building your AI
//See AI.h & AI.cpp for that
#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <iostream>
#include <vector>
#include <map>
#include <string>

#include "smartpointer.h"

namespace parser
{

const int ATTACK = 0;
const int DESTEALTH = 1;
const int MOVE = 2;
const int SELFDESTRUCT = 3;
const int STEALTH = 4;

struct Player
{
  int id;
  char* playerName;
  float time;
  int victories;
  int money;

  friend std::ostream& operator<<(std::ostream& stream, Player obj);
};

struct Ship
{
  int id;
  int owner;
  int x;
  int y;
  int radius;
  char* type;
  int attacksLeft;
  int movementLeft;
  int maxMovement;
  int maxAttacks;
  int damage;
  int health;
  int maxHealth;

  friend std::ostream& operator<<(std::ostream& stream, Ship obj);
};

struct ShipType
{
  int id;
  char* type;
  int cost;

  friend std::ostream& operator<<(std::ostream& stream, ShipType obj);
};


struct Animation
{
  int type;
};

struct attack : public Animation
{
  int acting;
  int target;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};

struct deStealth : public Animation
{
  int acting;

  friend std::ostream& operator<<(std::ostream& stream, deStealth obj);
};

struct move : public Animation
{
  int fromX;
  int fromY;
  int toX;
  int toY;
  int acting;

  friend std::ostream& operator<<(std::ostream& stream, move obj);
};

struct selfDestruct : public Animation
{
  int acting;

  friend std::ostream& operator<<(std::ostream& stream, selfDestruct obj);
};

struct stealth : public Animation
{
  int acting;

  friend std::ostream& operator<<(std::ostream& stream, stealth obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,Player> players;
  std::map<int,Ship> ships;
  std::map<int,ShipType> shipTypes;

  int turnNumber;
  int playerID;
  int gameNumber;
  int round;
  int victoriesNeeded;
  int mapRadius;

  std::map< int, std::vector< SmartPointer< Animation > > > animations;
  friend std::ostream& operator<<(std::ostream& stream, GameState obj);
};

struct Game
{
  std::vector<GameState> states;
  std::string players[2];
  int winner;
	std::string winReason;

  Game();
};

} // parser

#endif
