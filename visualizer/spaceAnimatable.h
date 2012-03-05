#ifndef CHESS_ANIMATABLE_H
#define CHESS_ANIMATABLE_H

#include "spaceAnimatable.h"
#include "irenderer.h"
#include "persistents.h"

#include "math.h"

namespace visualizer
{
    struct Background: public Animatable
    {
    };
    
    struct PersistentShipAnim: public Animatable
    {
    };
  
    struct SpaceShip: public Animatable
    {
        int id;
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
    
    struct AttackData: public Animatable
    {
        int attackerX;
        int attackerY;
        int victimX;
        int victimY;
        int attackerTeam;
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
