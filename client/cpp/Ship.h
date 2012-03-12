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
  ///The owner of the piece
  int owner();
  ///Position x
  int x();
  ///Position y
  int y();
  ///Ship size radius
  int radius();
  ///The ship type
  char* type();
  ///How many more attacks it has
  int attacksLeft();
  ///How much more movement it has
  int movementLeft();
  ///The largest possible movement
  int maxMovement();
  ///The max number of attacks it has
  int maxAttacks();
  ///The strength of its attacks
  int damage();
  ///The range of its attacks
  int range();
  ///The total health of the ship
  int health();
  ///The max health possible for the ship
  int maxHealth();
  ///The amount of damage done when this ship blows up
  int selfDestructDamage();
  ///Tells whether or not the ship is stealthed
  int isStealthed();
  ///Tells whether or not this ship is EMPd
  int isEMPd();

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

