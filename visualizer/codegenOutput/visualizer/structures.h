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

const int MOVE = 0;
const int SELFDESTRUCT = 1;
const int ATTACK = 2;
const int STEALTH = 3;
const int PLAYERTALK = 4;
const int DESTEALTH = 5;

struct ShipType
{
  int id;
  char* type;
  int cost;

  friend std::ostream& operator<<(std::ostream& stream, ShipType obj);
};

struct Player
{
  int id;
  char* playerName;
  float time;
  int victories;
  int energy;

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
  int range;
  int health;
  int maxHealth;
  int selfDestructDamage;

  friend std::ostream& operator<<(std::ostream& stream, Ship obj);
};


struct Animation
{
  int type;
};

struct move : public Animation
{
  int actingID;
  int fromX;
  int fromY;
  int toX;
  int toY;

  friend std::ostream& operator<<(std::ostream& stream, move obj);
};

struct selfDestruct : public Animation
{
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, selfDestruct obj);
};

struct attack : public Animation
{
  int actingID;
  int targetID;

  friend std::ostream& operator<<(std::ostream& stream, attack obj);
};

struct stealth : public Animation
{
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, stealth obj);
};

struct playerTalk : public Animation
{
  int actingID;
  char* message;

  friend std::ostream& operator<<(std::ostream& stream, playerTalk obj);
};

struct deStealth : public Animation
{
  int actingID;

  friend std::ostream& operator<<(std::ostream& stream, deStealth obj);
};


struct AnimOwner: public Animation
{
  int owner;
};

struct GameState
{
  std::map<int,ShipType> shipTypes;
  std::map<int,Player> players;
  std::map<int,Ship> ships;

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
