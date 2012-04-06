// -*-c++-*-

#ifndef SHIPDESCRIPTION_H
#define SHIPDESCRIPTION_H

#include <iostream>
#include "structures.h"


///Base class for all variables needed to define a ship
class ShipDescription {
  public:
  void* ptr;
  ShipDescription(_ShipDescription* ptr = NULL);

  // Accessors
  ///Unique Identifier
  int id();
  ///The ship type
  char* type();
  ///The amount of money required to purchase this type of ship
  int cost();
  ///The radius of the ship
  int radius();
  ///The range of attacks for this ship
  int range();
  ///The strength of attacks for this ship
  int damage();
  ///The amount of damage done when this ship self destructs
  int selfDestructDamage();
  ///The largest possible movement for this ship
  int maxMovement();
  ///The max number of attacks for this ship
  int maxAttacks();
  ///The max health possible for the ship
  int maxHealth();

  // Actions

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, ShipDescription ob);
};

#endif

