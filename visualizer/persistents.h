#ifndef PERSISTENTS_H
#define PERSISTENTS_H

#define M11  0.0    
#define M12  1.0   
#define M13  0.0   
#define M14  0.0   
#define M21 -0.5   
#define M22  0.0   
#define M23  0.5   
#define M24  0.0   
#define M31  1.0   
#define M32 -2.5   
#define M33  2.0   
#define M34 -0.5   
#define M41 -0.5   
#define M42  1.5   
#define M43 -1.5   
#define M44  0.5 


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
                
                int i = turn;
                
	            SpacePoint p;
	            int step = 1;
	            	
	            int v1 = i-step;		
	            int v2 = i;
	            int v3 = i+step;
	            int v4 = i+step*2;

	            if( i-step < 0 )
		            v1=0;
	            if( points.size() <= i+step )
		            v3=points.size()-1;
	            if( points.size() <= i+step*2 )
		            v4=points.size()-1;		
	            
	            double c1,c2,c3,c4;   

                c1 = M12*points[v2].x;   
                c2 = M21*points[v1].x + M23*points[v3].x;   
                c3 = M31*points[v1].x + M32*points[v2].x + M33*points[v3].x + M34*points[v4].x;   
                c4 = M41*points[v1].x + M42*points[v2].x + M43*points[v3].x + M44*points[v4].x;   

                float x = (((c4*t + c3)*t +c2)*t + c1);

                c1 = M12*points[v2].y;   
                c2 = M21*points[v1].y + M23*points[v3].y;   
                c3 = M31*points[v1].y + M32*points[v2].y + M33*points[v3].y + M34*points[v4].y;   
                c4 = M41*points[v1].y + M42*points[v2].y + M43*points[v3].y + M44*points[v4].y;   

                float y = (((c4*t + c3)*t +c2)*t + c1);

                return SpacePoint( x, y );
            }
            
            float HeadingOn(int turn, float t)
            {
                turn -= createdAtTurn;
                
                int i = turn;

	            int step = 1;
	            	
	            int v1 = i-step;		
	            int v2 = i;
	            int v3 = i+step;
	            int v4 = i+step*2;

	            if( i-step < 0 )
		            v1=0;
	            if( points.size() <= i+step )
		            v3=points.size()-1;
	            if( points.size() <= i+step*2 )
		            v4=points.size()-1;		
	            
	            double c1,c2,c3,c4;   

                c1 = M12*points[v2].x;   
                c2 = M21*points[v1].x + M23*points[v3].x;   
                c3 = M31*points[v1].x + M32*points[v2].x + M33*points[v3].x + M34*points[v4].x;   
                c4 = M41*points[v1].x + M42*points[v2].x + M43*points[v3].x + M44*points[v4].x;   

                float x = (3*c4*t + 2*c3)*t +c2;

                c1 = M12*points[v2].y;   
                c2 = M21*points[v1].y + M23*points[v3].y;   
                c3 = M31*points[v1].y + M32*points[v2].y + M33*points[v3].y + M34*points[v4].y;   
                c4 = M41*points[v1].y + M42*points[v2].y + M43*points[v3].y + M44*points[v4].y;   

                float y = (3*c4*t + 2*c3)*t +c2;

                return atan2( y, x );
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
