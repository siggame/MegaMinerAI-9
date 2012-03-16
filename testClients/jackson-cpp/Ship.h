// -*-c++-*-

#ifndef SHIP_H
#define SHIP_H

#include <iostream>
#include "structures.h"

class Ship;

///A space ship!
class Ship {
  public:
  void* ptr;
  Ship(_Ship* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The owner of the ship
  int owner();
  ///X position of the ship
  int x();
  ///Y position of the ship
  int y();
  ///The radius of the ship
  int radius();
  ///The ship type
  char* type();
  ///How many more attacks this ship has
  int attacksLeft();
  ///How much more movement this ship has
  int movementLeft();
  ///The largest possible movement for this ship
  int maxMovement();
  ///The max number of attacks for this ship
  int maxAttacks();
  ///The strength of attacks for this ship
  int damage();
  ///The range of attacks for this ship
  int range();
  ///The total health of the ship
  int health();
  ///The max health possible for the ship
  int maxHealth();
  ///The amount of damage done when this ship self destructs
  int selfDestructDamage();

  // Actions
  ///Command a ship to move to a specified position
  int move(int x, int y);
  ///Blow yourself up, damage those around you
  int selfDestruct();
  ///Commands your ship to attack a target
  int attack(Ship& target);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Ship ob);
};

#endif

