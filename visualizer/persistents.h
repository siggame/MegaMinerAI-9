#ifndef PERSISTENTS_H
#define PERSISTENTS_H

#include "parser/structures.h"
#include <vector>
#include <math.h>
#include <map>
#include <utility>

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
                
                // have it stealth now (only Stealth ships care...)
                AddStealth( createdAt );
            }
            
            // Stats that change each turn
            vector< SpacePoint > points;
            vector< int > healths;
            
            bool ExistsAtTurn(int turn)
            {
                return ( turn >= createdAtTurn && turn < createdAtTurn + (int)healths.size() );
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
                t = 0;
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
            
            void AddStealth( int turn )
            {
                m_Stealths.push_back( pair<int,char>(turn, 's') );
            }
            
            void AddDeStealth( int turn )
            {
                m_Stealths.push_back( pair<int,char>(turn, 'd') );
            }
            
            float StealthOn( int turn, float t)
            {
                // if this is not a stealth ship just return 1, as other's can't stealth
                if(strcmp("Stealth", type.c_str()) != 0)
                {
                    return 1;
                }
                
                for(int i = 0; i < (int)m_Stealths.size(); i++)
                {
                    // if the current turn is the turn it stealthed or destealthed
                    if(m_Stealths[i].first == turn)
                    {
                        return (m_Stealths[i].second == 'd' ? (t * 0.75f) + 0.25f : 1 - (t * 0.75f));
                    }
                    
                    // if the turn it did something is larger than the current turn, it is in the state last time it did something
                    if(m_Stealths[i].first > turn)
                    {
                        if(i == 0) // if the turn that is larger is so far in the future the ship hasn't done anything else, it's stealthed
                        {
                            return 0.25f;
                        }
                        else // else return if it currently stealthed or not stealthed based on the last stealth animation
                        {
                            return (m_Stealths[i - 1].second == 'd' ? 1.0f : 0.25f);
                        }
                    }
                }
                
                cout << "Stealth: should not reach here?" << endl;
                return 0.25f;
                
            }
            
            float ExplodingOn( int turn )
            {
                return (healths[turn - createdAtTurn] == 0);
            }
            
            void Finalize()
            {
                healths.push_back(0);
                points.push_back( SpacePoint( points.back().x, points.back().y ) );
            }
            
        private:
            int createdAtTurn;
            map< int, vector< SpacePoint > > m_AttackLocations;
            vector< pair< int, char > > m_Stealths;  // int represents the turn, char 's' represents that it went into stealth, 'd' is destealth
            
            int PreviousTurn(int turn)
            {
                return (turn > 0 ? turn - 1 : 0);
            }
            
            
    };
}

#endif  // PERSISTENTS
