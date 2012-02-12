#ifndef CHESS_ANIMATABLE_H
#define CHESS_ANIMATABLE_H

#include "spaceAnimatable.h"
#include "irenderer.h"

namespace visualizer
{
    struct Background: public Animatable
    {
    };
  
    struct SpaceShip: public Animatable
    {
        int owner;
        int x;
        int y;
        int radius;
        string type;
        int attacksLeft;
        int movementLeft;
        int maxMovement;
        int maxAttacks;
        int damage;
        int range;
        int health;
        int maxHealth;
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
