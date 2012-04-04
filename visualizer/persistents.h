#ifndef PERSISTENTS_H
#define PERSISTENTS_H
#include "parser/structures.h"
#include <vector>
#include <math.h>
#include <map>
#include <utility>
#include <sstream>
#include "glm/glm.hpp"
#include "glm/gtx/vector_angle.hpp"

using glm::vec2;

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

namespace visualizer
{
  ostream& operator <<( ostream& os, const vec2& v );
  ostream& operator <<( ostream& os, const glm::vec4& v );
  ostream& operator <<( ostream& os, const glm::mat4x2& m );
  ostream& operator <<( ostream& os, const glm::mat4& m );

  const auto A = glm::mat4( 
      1, 0, 0, 0,
      0, 1, 0, 0, 
      -3, -2, 3, -1, 
      2, 1, -2, 1
      );

  class SpaceMove
  {
    public:
      vec2 point;
      float start;
      float end;

      bool InRange(float time) { return start < time && end >= time; }
      bool IsAfter(float time) { return start > time; }
      bool IsBefore(float time) { return end < time; }
  };


  struct TempShip
  {
    vec2 position;
    float radius;
    int id;
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
      int maxMovement;
      string type;
      bool selected;

      PersistentShip(int createdAt, int round, parser::Ship ship)
      {
        createdAtTurn = createdAt;
        id = ship.id;
        owner = ship.owner;
        radius = ship.radius;
        range = ship.range;
        maxHealth = ship.maxHealth;
        type = (ship.type == NULL ? "default" : ship.type);
        maxMovement = ship.maxMovement;
        m_InitialX = ship.x;
        m_InitialY = ship.y;
        m_Round = round;
        selected = false;
        m_DeathTurn = 99999;
        
        if( strcmp( "Mine", type.c_str() ) == 0 )
          radius /= 2.0f;

        // have it stealth now (only Stealth ships care...)
        AddStealth( createdAt );
      }

      // Stats that change each turn
      vector<vec2> points;
      vector<int> healths;
      vector<bool> emps;

      void AddTurn(int turn, vector<vec2> &moves, int movementLeft)
      {
        float span = 1.0f;// / moves.size();
        for(float i = 0; i < (float)moves.size(); i++)
        {
          if( i != 0 )
            continue;
            
          SpaceMove move;
          move.point = moves[i];
          move.start = (float)turn + i * span;
          move.end = (float)turn + (i+1) * span;

          m_Moves.push_back( move );
        }
        
        m_MovementLeft.push_back( movementLeft );
      }

      bool HasMoves() { return m_Moves.size() > 0; }

      bool ExistsAtTurn(int turn, int round)
      {
        return ( turn >= createdAtTurn && turn <= m_DeathTurn && (m_Round == round || round == -1) );
      }

      vec2 LocationOn(int turn, float t)
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
        //turn -= createdAtTurn;
        //return emps[turn];
        return false;
      }

      vector<vec2> AttacksOn( int turn, float t )
      {
        if( m_AttackVictims.find( turn ) == m_AttackVictims.end() )
          return vector<vec2>();

        // else, find every victim's location
        vector<vec2> victimLocations;

        for(unsigned int i = 0; i < m_AttackVictims[turn].size(); i++)
        {
          victimLocations.push_back(m_AttackVictims[turn][i]->LocationOn(turn, t));
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

      float StealthOn( int /*turn*/, float /*t*/)
      {
        return (strcmp("Stealth", type.c_str()) != 0) ? 1 : 0.3f;
      }

      float ExplodingOn( int turn )
      {
        return turn == m_DeathTurn;
      }

      bool RenderShield()
      {
        return !(strcmp( "Mine", type.c_str() ) == 0);
      }

      bool RenderRange()
      {
        return (strcmp( "Mine", type.c_str() ) == 0) || (strcmp( "Support", type.c_str() ) == 0) || (strcmp( "Warp Gate", type.c_str() ) == 0);
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
          pts << "(" << points[turn-createdAtTurn].x << "," << points[turn-createdAtTurn].y << ")";
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
      
      string MovementOn( int turn )
      {
        turn -= createdAtTurn;
        stringstream ss;
        if( turn >= m_MovementLeft.size() || turn < 0 )
        {
          ss << "-1/" << maxMovement;
          return ss.str();
        }
        
        ss << m_MovementLeft[ turn ] << "/" << maxMovement;
        return ss.str();
      }
      
      void AddDeath( int turn )
      {
        m_DeathTurn = turn;
        healths.push_back( 0 );
        points.push_back(vec2( points.back().x, points.back().y ));
        
        if(m_Moves.size() > 0)
        {
          SpaceMove move;
          move.point.x = m_Moves.back().point.x;
          move.point.y = m_Moves.back().point.y;
          move.start = m_Moves.back().end;
          move.end = m_Moves.back().end + 2;
          
          m_Moves.push_back( move );
        }
      }
    
    private:
      int createdAtTurn;
      float m_InitialX;
      float m_InitialY;

      map< int, vector < PersistentShip* > > m_AttackVictims;
      vector< pair< int, char > > m_Stealths;  // int represents the turn, char 's' represents that it went into stealth, 'd' is destealth
      vector< SpaceMove > m_Moves;
      int m_Round;
      vector<int> m_MovementLeft;
      int m_DeathTurn;

      int PreviousTurn(int turn)
      {
        return (turn > 0 ? turn - 1 : 0);
      }

      pair<vec2, float> GardnersSplineOn(int turn, float t)
      {
        // Index setup from Jake F. 
        
        turn -= createdAtTurn;
        int i = turn;
        const int step = 1;
        int v0 = i-step;
        int v1 = i;
        int v2 = i+step;
        int v3 = i+2*step;

        if( i-step < 0 )
          v0=0;
        if( (signed)points.size() <= i+step )
          v2=points.size()-1;
        if( (signed)points.size() <= i+step*2 )
          v3=points.size()-1;		

        // Setting up the verticies

        auto times = glm::vec4(1, t, t*t, t*t*t);
        auto p0 = vec2(points[v1].x, points[v1].y);
        auto p1 = vec2(points[v2].x, points[v2].y);
        auto m0 = glm::normalize(p0 - vec2(points[v0].x, points[v0].y));
        auto m1 = glm::normalize(vec2(points[v3].x, points[v3].y) - p1);

        if( m0.x != m0.x )
          m0 = vec2(0, 0);

        if( m1.x != m1.x )
          m1 = vec2(0, 0);

        m0 *= 0;
        m1 *= 0;

        auto q = glm::mat4x2(p0, m0, p1, m1);

        glm::vec4 m = times * glm::transpose(A);
        vec2 result = q * m;
      
        double angle = glm::orientedAngle(vec2(1,0), glm::normalize(p1-p0));
        if( angle != angle )
          angle = 0;
        cout << angle << endl;
        return make_pair(vec2(result.x, result.y), angle);
      }
      
      pair<vec2, float> SplineOn(int turn, float t)
      {
        int v2 = -1;
        float time = float(turn) + t;

        if(m_Moves.size() == 0)
          return make_pair(vec2( m_InitialX, m_InitialY ), 0);
        
        int i = -1;
        for(i = 0; i < m_Moves.size(); i++)
        {
          if( m_Moves[i].InRange( time ) )
          {
            v2 = i;
            i = m_Moves.size();
          }
          else if( m_Moves[i].start > time )
          {
            v2 = i-1;
            t = 1.0f;
            i = m_Moves.size();
          }
          else if( m_Moves[i].end < time )
          {
            continue;
          }
          else
          {
            THROW(Exception, "Shouldn't Happen");
              // Shouldn't happen
          }
        }
        
        if(i == m_Moves.size()-1 && v2 == -1)
        {
          v2 = m_Moves.size()-1;
        }
        
        int v1 = v2-1;
        int v3 = v2+1;
        int v4 = v2+2;

        if( v1 < 0 )
          v1=0;
        if( v2 < 0 )
          v2=0;
        if( m_Moves.size() <= v3 )
          v3=m_Moves.size()-1;
        if( m_Moves.size() <= v4 )
          v4=m_Moves.size()-1;		
        
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

        return make_pair(vec2(px, py), atan2(hy, hx));
      }
      
  };
}

#endif  // PERSISTENTS
