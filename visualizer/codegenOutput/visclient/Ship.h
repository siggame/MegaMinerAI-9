// -*-c++-*-

#ifndef SHIP_H
#define SHIP_H

#include <iostream>
#include "vc_structures.h"


namespace client
{

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
  ///ship size radius
  int radius();
  ///The ship type
  char* type();
  ///how many more attacks it has
  int attacksLeft();
  ///how much more movement it has
  int movementLeft();
  ///the largest possible movement
  int maxMovement();
  ///the max number of attacks it has
  int maxAttacks();
  ///the strength of its attacks
  int damage();
  ///the total health of the ship
  int health();
  ///the max health possible for the ship
  int maxHealth();

  // Actions
  ///
  int move(int x, int y);
  ///
  int selfDestruct();
  ///
  int attack(Ship& target);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, Ship ob);
};

}

#endif

