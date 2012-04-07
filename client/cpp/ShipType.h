// -*-c++-*-

#ifndef SHIPTYPE_H
#define SHIPTYPE_H

#include <iostream>
#include "structures.h"

#include "ShipDescription.h"

///An available ship type
class ShipType : public ShipDescription {
  public:
  ShipType(_ShipType* ptr = NULL);

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
  ///Sends in a new ship of this type. Ships must be warped in with the radius of the player's warp ship.
  int warpIn(int x, int y);

  // Properties


  friend std::ostream& operator<<(std::ostream& stream, ShipType ob);
};

#endif

