#ifndef PERSISTENTS_H
#define PERSISTENTS_H

#include "parser/structures.h"

namespace visualizer
{
    class SpacePoint
    {
        public: 
            float x;
            float y;
            
            SpacePoint()
            {
                x = y = 0;
            }
            
            SpacePoint(int posX, int posY)
            {
                x = posX;
                y = posY;
            }
            
            SpacePoint(float posX, float posY)
            {
                x = posX;
                y = posY;
            }
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
            
            PersistentShip(int createdAt, parser::Ship ship)
            {
                createdAtTurn = createdAt;
                id = ship.id;
                owner = ship.owner;
                radius = ship.radius;
                range = ship.range;
                maxHealth = ship.maxHealth;
                type = (ship.type == NULL ? "default" : ship.type);
            }
            
            // Stats that change each turn
            vector< SpacePoint > points;
            vector< int > healths;
            
            bool ExistsAtTurn(int turn)
            {
                return ( turn >= createdAtTurn && turn < createdAtTurn + healths.size() );
            }
            
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
            
            float HealthAt(int turn, float t)
            {
                turn -= createdAtTurn;
                
                // h(t) = a + t(b - a)
                return healths[PreviousTurn(turn)] + t * ( healths[turn] - healths[PreviousTurn(turn)] );
            }
        private:
            int createdAtTurn;
            
            int PreviousTurn(int turn)
            {
                return (turn > 0 ? turn - 1 : 0);
            }
    };
}

#endif  // PERSISTENTS
