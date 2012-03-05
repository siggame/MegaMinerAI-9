#ifndef PERSISTENTS_H
#define PERSISTENTS_H

#include "parser/structures.h"
#include <vector>
#include <math.h>
#include <map>

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
            
            SpacePoint LocationOn(int turn, float t)
            {
                turn -= createdAtTurn;
                
                // Equation of a line: r(t) = a+t(b-a)
                //   where a is the start postion and b is the end
                SpacePoint location;
                
                location.x = points[PreviousTurn(turn)].x + t * (points[turn].x - points[PreviousTurn(turn)].x);
                location.y = points[PreviousTurn(turn)].y + t * (points[turn].y - points[PreviousTurn(turn)].y);
                
                return location;
            }
            
            float HeadingOn(int turn, float t)
            {
                // ATan2(dy , dx) where dy = y2 - y1 and dx = x2 - x1
                turn -= createdAtTurn;
                
                return atan2( points[turn].y - points[PreviousTurn(turn)].y, points[turn].x - points[PreviousTurn(turn)].x );
            }
            
            float HealthOn(int turn, float t)
            {
                turn -= createdAtTurn;
                
                // h(t) = a + t(b - a)
                return healths[PreviousTurn(turn)] + t * ( healths[turn] - healths[PreviousTurn(turn)] );
            }
            
            vector< SpacePoint > AttacksOn(int turn)
            {
                if( m_AttackLocations.find( turn ) == m_AttackLocations.end() )
                    return vector< SpacePoint>();
                else
                    return m_AttackLocations[turn];
            }
            
            void AddAttack( parser::Ship victim, int turn)
            {
                if(AttacksOn(turn).size() > 0)
                {
                    m_AttackLocations[turn] = vector< SpacePoint >(); 
                }
                
                m_AttackLocations[turn].push_back( SpacePoint( victim.x, victim.y ) );
            }
            
            
        private:
            int createdAtTurn;
            map< int, vector< SpacePoint > > m_AttackLocations;
            
            int PreviousTurn(int turn)
            {
                return (turn > 0 ? turn - 1 : 0);
            }
            
            
    };
}

#endif  // PERSISTENTS
