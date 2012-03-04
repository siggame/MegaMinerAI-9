#ifndef CHESS_ANIMATABLE_H
#define CHESS_ANIMATABLE_H

#include "spaceAnimatable.h"
#include "irenderer.h"

#include "math.h"

namespace visualizer
{
    struct SpacePoint
    {
        float x;
        float y;
    };  
    
    struct Background: public Animatable
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
    
    class PersistentShip
    {
        public:
            // stats that never change
            int id;
            int owner;
            int radius;
            int range;
            int maxHealth;
            string type;
            
            PersistentShip(int createdAt)
            {
                createdAtTurn = createdAt;
            }
            
            // Stats that change each turn
            vector< SpacePoint > points;
            vector< int > healths;
            
            SpacePoint LocationAt(int turn, float t)
            {
                turn -= createdAtTurn;
                
                // Equation of a line: r(t) = a+t(b-a)
                //   where a is the start postion and b is the end
                SpacePoint location;
                
                location.x = points[PreviousTurn(turn)].x + t * (points[turn].x - points[PreviousTurn(turn)].x);
                location.y = points[PreviousTurn(turn)].y + t * (points[turn].y - points[PreviousTurn(turn)].y);
                
                return location;
            }
            
            float HeadingAt(int turn, float t)
            {
                // ATan2(dy , dx) where dy = y2 - y1 and dx = x2 - x1
                turn -= createdAtTurn;
                
                return atan2( points[turn].y - points[PreviousTurn(turn)].y, points[turn].x - points[PreviousTurn(turn)].x );
            }
        private:
            int createdAtTurn;
            
            int PreviousTurn(int turn)
            {
                return (turn > 0 ? turn - 1 : 0);
            }
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
