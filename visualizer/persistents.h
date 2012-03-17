#ifndef PERSISTENTS_H
#define PERSISTENTS_H

#if 1
#define M11  0.0    
#define M21 -0.5   
#define M31  1.0   
#define M41 -0.5   

#define M12  1.0   
#define M22  0.0   
#define M32 -2.5   
#define M42  1.5   

#define M13  0.0   
#define M23  0.5   
#define M33  2.0   
#define M43 -1.5   

#define M14  0.0   
#define M24  0.0   
#define M34 -0.5   
#define M44  0.5 
#else
// Official Cubic Hermite Spline Equation
// See wiki
#define M11  0.0   
#define M21  1.0   
#define M31 -2.0   
#define M41  1.0   

#define M12  1.0    
#define M22  0.0   
#define M32 -3.0   
#define M42  2.0   

#define M13  0.0   
#define M23  0.0   
#define M33  3.0   
#define M43 -2.0   

#define M14  0.0   
#define M24  0.0   
#define M34 -1.0   
#define M44  1.0 
#endif

#include "parser/structures.h"
#include <vector>
#include <math.h>
#include <map>
#include <utility>
#include <sstream>

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
            
            void operator=( const SpacePoint & rhs )
            {
                x = rhs.x;
                y = rhs.y;
            }
    };  
    
    class SpaceMove
    {
        public:
            SpacePoint point;
            float start;
            float end;
            
            bool InRange(float time) { return start < time && end >= time; }
            bool IsAfter(float time) { return start > time; }
            bool IsBefore(float time) { return end < time; }
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
            
            PersistentShip(int createdAt, int round, parser::Ship ship)
            {
                createdAtTurn = createdAt;
                id = ship.id;
                owner = ship.owner;
                radius = ship.radius;
                range = ship.range;
                maxHealth = ship.maxHealth;
                type = (ship.type == NULL ? "default" : ship.type);
                m_X = ship.x;
                m_Y = ship.y;
                m_Round = round;
                
                // have it stealth now (only Stealth ships care...)
                AddStealth( createdAt );
            }
            
            // Stats that change each turn
            vector< SpacePoint > points;
            vector< int > healths;
            vector< bool > emps;
            
            void AddTurn( int turn, vector< SpacePoint > &moves )
            {
                float span = 1.0f / moves.size();
                for(float i = 0; i < (float)moves.size(); i++)
                {
                    SpaceMove move;
                    move.point = moves[i];
                    move.start = (float)turn + i * span;
                    move.end = (float)turn + (i+1) * span;
                    
                    m_Moves.push_back( move );
                }
            }
            
            bool HasMoves() { return m_Moves.size() > 0; }
            
            bool ExistsAtTurn(int turn, int round)
            {
                return ( turn >= createdAtTurn && turn < createdAtTurn + (int)healths.size() && m_Round == round );
            }
            
            SpacePoint LocationOn(int turn, float t)
            {
                auto lah = SplineOn(turn, t);
                return lah.first;
            }
            
            float HeadingOn(int turn, float t)
            {
                auto lah = SplineOn(turn, t);
                return lah.second;
            }
            
            float HealthOn(int turn, float t)
            {
                turn -= createdAtTurn;
                
                // h(t) = a + t(b - a)
                return healths[PreviousTurn(turn)] + t * ( healths[turn] - healths[PreviousTurn(turn)] );
            }
            
            bool EMPedOn(int turn)
            {
                turn -= createdAtTurn;
                return emps[turn];
            }
            
            /*vector< SpacePoint > AttacksOn(int turn)
            {
                if( m_AttackLocations.find( turn ) == m_AttackLocations.end() )
                    return vector< SpacePoint>();
                else
                    return m_AttackLocations[turn];
            }*/
            
            /*void AddAttack( parser::Ship victim, int turn)
            {
                if(AttacksOn(turn).size() > 0)
                {
                    m_AttackLocations[turn] = vector< SpacePoint >(); 
                }
                
                m_AttackLocations[turn].push_back( SpacePoint( victim.x, victim.y ) );
            }*/
            
            vector< SpacePoint > AttacksOn( int turn, float t )
            {
                if( m_AttackVictims.find( turn ) == m_AttackVictims.end() )
                    return vector< SpacePoint >();
                
                // else, find every victim's location
                vector< SpacePoint > victimLocations;
                
                for(unsigned int i = 0; i < m_AttackVictims[turn].size(); i++)
                {
                    victimLocations.push_back( m_AttackVictims[turn][i]->LocationOn( turn, t ) );
                }
                
                return victimLocations;
            }
            
            void AddAttack( PersistentShip* victim, int turn )
            {
                if(m_AttackVictims.find( turn ) == m_AttackVictims.end())
                {
                    m_AttackVictims[turn] = vector< PersistentShip* >(); 
                }
                
                m_AttackVictims[turn].push_back( victim );
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
                return (strcmp("Stealth", type.c_str()) != 0) ? 1 : 0.3f;
            }
            
            float ExplodingOn( int turn )
            {
                return (healths[turn - createdAtTurn] == 0);
            }
            
            void Finalize()
            {
                healths.push_back(0);
                points.push_back( SpacePoint( points.back().x, points.back().y ) );
                
                for(int i = 0; i < m_Moves.size(); i++)
                {
                    cout << id << ": #" << i << ":  (" << m_Moves[i].point.x << "," << m_Moves[i].point.y << ") @" << m_Moves[i].start << " to " << m_Moves[i].end << endl;
                }
                
            }
            
            bool RenderShield()
            {
                return !(strcmp( "Mine", type.c_str() ) == 0);
            }
            
            bool RenderRange()
            {
                return (strcmp( "Mine", type.c_str() ) == 0) || (strcmp( "Support", type.c_str() ) == 0);
            }
            
            string PointsOn( int turn )
            {
                stringstream pts;
                
                bool nothing = true;
                for( auto& spacemove : m_Moves )
                {
                    if( (int)spacemove.start == turn - 1)
                    {
                        pts << "(" << spacemove.point.x << "," << spacemove.point.y << ")";
                        nothing = false;
                    }
                    else if( spacemove.start > (float)turn )
                    {
                        break;
                    }
                }
                
                // if it didn't move in that timespan
                if( nothing )
                {
                    pts.str("");
                    pts << "(" << m_X << "," << m_Y << ")";
                }
                
                return pts.str();
            }
            
            string AttacksWhoOn( int turn )
            {
                if( m_AttackVictims.find( turn ) == m_AttackVictims.end() )
                    return "none";
                
                stringstream victims;
                
                for(unsigned int i = 0; i < m_AttackVictims[turn].size()-1; i++)
                {
                    victims << m_AttackVictims[turn][i]->id << ", ";
                }
                
                victims << m_AttackVictims[turn].back()->id;
                
                return victims.str();
            }
            
        private:
            int createdAtTurn;
            float m_X;
            float m_Y;
            //map< int, vector< SpacePoint > > m_AttackLocations;
            map< int, vector < PersistentShip* > > m_AttackVictims;
            vector< pair< int, char > > m_Stealths;  // int represents the turn, char 's' represents that it went into stealth, 'd' is destealth
            vector< SpaceMove > m_Moves;
            int m_Round;
            
            int PreviousTurn(int turn)
            {
                return (turn > 0 ? turn - 1 : 0);
            }
            
            pair<SpacePoint, float> SplineOn(int turn, float t)
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

                float px = (((c4*t + c3)*t +c2)*t + c1);
                float hx = (3*c4*t + 2*c3)*t +c2;

                c1 = M12*points[v2].y;   
                c2 = M21*points[v1].y + M23*points[v3].y;   
                c3 = M31*points[v1].y + M32*points[v2].y + M33*points[v3].y + M34*points[v4].y;   
                c4 = M41*points[v1].y + M42*points[v2].y + M43*points[v3].y + M44*points[v4].y;   

                float py = (((c4*t + c3)*t +c2)*t + c1);
                float hy = (3*c4*t + 2*c3)*t +c2;

                return make_pair( SpacePoint( px, py ), atan2( hy, hx ) );
            }
            
            pair<SpacePoint, float> NewSplineOn(int turn, float t)
            {
                if( m_Moves.size() == 0 )
                {
                    return make_pair( SpacePoint( m_X, m_Y ), 0.0f );
                }
                
                int v1 = -1, v2 = -1, v3 = -1, v4 = -1;
                float time = (float)turn + t;
                bool needNewT = true;
                
                for(int i = 0; i < m_Moves.size(); i++)
                {
                    if( m_Moves[i].InRange( time ) )
                    {
                        v2 = i;
                        break;
                    }
                    else if( m_Moves[i].IsAfter( time ) )
                    {
                        if( i == 0 )
                        {
                            v2 = 0;
                            break;
                        }
                        
                        if( m_Moves[i - 1].IsBefore( time ) )
                        {
                            v2 = i - 1;
                            t = 1;
                            needNewT = false;
                            break;
                        }
                    }
                }
                
	            v1 = v2-1;
	            v3 = v2+1;
	            v4 = v2+2;

	            if( v1 < 0 )
		            v1=0;
	            if( v2 < 0 )
	                v2=0;
	            if( m_Moves.size() <= v3 )
		            v3=m_Moves.size()-1;
	            if( m_Moves.size() <= v4 )
		            v4=m_Moves.size()-1;		
	            
	            if( needNewT )
	            {
	                // new_t = (t - start) / (end - start)
	                int dt = int(m_Moves[v2].start);
	                t = (t - (m_Moves[v2].start - dt)) / ( (m_Moves[v2].end - dt) - (m_Moves[v2].start - dt) );
	                if(t > 1 || t < 0)
	                {
	                    cout << "WTF t is: " << t << endl;
	                }
	            }
	            
	            double c1,c2,c3,c4;   

                c1 = M12*m_Moves[v2].point.x;   
                c2 = M21*m_Moves[v1].point.x + M23*m_Moves[v3].point.x;   
                c3 = M31*m_Moves[v1].point.x + M32*m_Moves[v2].point.x + M33*m_Moves[v3].point.x + M34*m_Moves[v4].point.x;   
                c4 = M41*m_Moves[v1].point.x + M42*m_Moves[v2].point.x + M43*m_Moves[v3].point.x + M44*m_Moves[v4].point.x;   

                float px = (((c4*t + c3)*t +c2)*t + c1);
                float hx = (3*c4*t + 2*c3)*t +c2;

                c1 = M12*m_Moves[v2].point.y;   
                c2 = M21*m_Moves[v1].point.y + M23*m_Moves[v3].point.y;   
                c3 = M31*m_Moves[v1].point.y + M32*m_Moves[v2].point.y + M33*m_Moves[v3].point.y + M34*m_Moves[v4].point.y;   
                c4 = M41*m_Moves[v1].point.y + M42*m_Moves[v2].point.y + M43*m_Moves[v3].point.y + M44*m_Moves[v4].point.y;   

                float py = (((c4*t + c3)*t +c2)*t + c1);
                float hy = (3*c4*t + 2*c3)*t +c2;

                return make_pair( SpacePoint( px, py ), atan2( hy, hx ) );
            }
    };
}

#endif  // PERSISTENTS
