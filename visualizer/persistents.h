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
  ostream& operator <<( ostream& os, const glm::vec2& v );
  ostream& operator <<( ostream& os, const glm::vec4& v );
  ostream& operator <<( ostream& os, const glm::mat4x2& m );
  ostream& operator <<( ostream& os, const glm::mat4& m );

  const auto A = glm::mat4( 
      1, 0, 0, 0,
      0, 1, 0, 0, 
      -3, -2, 3, -1, 
      2, 1, -2, 1
      );

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
      int maxMovement;
      string type;
      bool selected;
      bool SelfDestructs;

      PersistentShip(int createdAt, int round, parser::Ship ship)
      {
        m_CreatedAtTurn = createdAt+1;
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
        SelfDestructs = false;
        
        if( strcmp( "Mine", type.c_str() ) == 0 )
          radius /= 2.0f;
      }

      void AddTurn( int turn, vector< SpacePoint > &moves, int health, int movementLeft )
      {
        // Add the moves
        float span = 1.0f / float(moves.size());
        for(float i = 0; i < (float)moves.size(); i++)
        {
          SpaceMove move;
          move.point = moves[i];
          move.start = (float)turn + i * span;
          move.end = (float)turn + (i+1) * span;
          
          // to stop duplicate move to the same location in the same turn... because that is apperntly happening on the first turn.
          if(m_Moves.size() > 0)
          {
            if(m_Moves.back().point.x != move.point.x && m_Moves.back().point.y != move.point.y)
            {
              m_Moves.push_back( move );
            }
          }
          else
          {
            m_Moves.push_back( move );
          }
        }
        
        if( turn >= m_CreatedAtTurn )
        {
          // Add the movement left
          m_MovementLeft.push_back( movementLeft );
          
          // Add the health this turn
          m_Healths.push_back( health );
        }
      }

      bool HasMoves() { return m_Moves.size() > 0; }

      bool ExistsAtTurn(int turn, int round)
      {
        return ( turn >= m_CreatedAtTurn && turn <= m_DeathTurn && (m_Round == round || round == -1) );
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
        turn -= m_CreatedAtTurn;

        // h(t) = a + t(b - a)
        return m_Healths[PreviousTurn(turn)] + t * ( m_Healths[turn] - m_Healths[PreviousTurn(turn)] );
      }

      bool EMPedOn(int turn)
      {
        //for( auto& empedTurn : m_EMPeds )
        for( int i = 0; i < m_EMPeds.size(); i++ )
        {
          int empedTurn = m_EMPeds[i];
          if( empedTurn == turn )
          {
            return true;
          }
        }
        
        return false;
      }

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
      
      void AddEMPed( int turn )
      {
        m_EMPeds.push_back( turn );
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
          auto location = SplineOn( turn, 1.0f ).first;
          pts << "(" << location.x << "," << location.y << ")";
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
        turn -= m_CreatedAtTurn;
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
        m_Healths.push_back( 0 );
        
        /*if(m_Moves.size() > 0)
        {
          SpaceMove move;
          move.point.x = m_Moves.back().point.x;
          move.point.y = m_Moves.back().point.y;
          move.start = m_Moves.back().end;
          move.end = m_Moves.back().end + 2;
          
          m_Moves.push_back( move );
        }*/
      }
      
      int FirstTurn() { return m_CreatedAtTurn; }
      
      void MoveInfo()
      {        
        cout << "Ship " << id << " of type " << type << endl;
        
        for( auto& move : m_Moves )
        {
          cout << "  (" << move.point.x << "," << move.point.y << ") from " << move.start << " to " << move.end << endl;
        }
      }
      
    private:
      int m_CreatedAtTurn;
      vector< int > m_Healths;
      float m_InitialX;
      float m_InitialY;
      map< int, vector < PersistentShip* > > m_AttackVictims;
      vector< pair< int, char > > m_Stealths;  // int represents the turn, char 's' represents that it went into stealth, 'd' is destealth
      vector< SpaceMove > m_Moves;
      int m_Round;
      vector<int> m_MovementLeft;
      int m_DeathTurn;
      vector< int > m_EMPeds;

      int PreviousTurn(int turn)
      {
        return (turn > 0 ? turn - 1 : 0);
      }

      /*pair<SpacePoint, float> GardnersSplineOn(int turn, float t)
      {
        // Index setup from Jake F. 
        
        turn -= m_CreatedAtTurn;
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
        auto p0 = glm::vec2(points[v1].x, points[v1].y);
        auto p1 = glm::vec2(points[v2].x, points[v2].y);
        auto m0 = glm::normalize(p0 - glm::vec2(points[v0].x, points[v0].y));
        auto m1 = glm::normalize(glm::vec2(points[v3].x, points[v3].y) - p1);

        if( m0.x != m0.x )
          m0 = glm::vec2(0, 0);

        if( m1.x != m1.x )
          m1 = glm::vec2(0, 0);

        m0 *= 0;
        m1 *= 0;

        auto q = glm::mat4x2(p0, m0, p1, m1);

        glm::vec4 m = times * glm::transpose(A);
        glm::vec2 result = q * m;
      
        double angle = glm::orientedAngle(glm::vec2(1,0), glm::normalize(p1-p0));
        if( angle != angle )
          angle = 0;
        cout << angle << endl;
        return make_pair(SpacePoint(result.x, result.y), angle);
      }*/
      
      pair<SpacePoint, float> SplineOn(int turn, float t)
      {
        int v1, v2, v3, v4;
        v1 = v2 = v3 = v4 = -1;
        bool foundV3 = false;

        float time = float(turn) + t;
        if(m_Moves.size() == 0)
          return make_pair( SpacePoint( m_InitialX, m_InitialY ), 0 );
        
        for(int i = 0; i < m_Moves.size(); i++)
        {
          if( m_Moves[i].InRange( time ) )
          {
            v3 = i;
            i = m_Moves.size();
            foundV3 = true;
          }
          else if( m_Moves[i].start > time )
          {
            v3 = i-1;
            t = 1.0f;
            i = m_Moves.size();
            foundV3 = true;
          }
          else if( m_Moves[i].end < time )
          {
            continue;
          }
          else
          {
              // Shouldn't happen
          }
        }

        if( !foundV3 )
        {
          v3 = m_Moves.size()-1;
          t = 1.0f;
        }
        
        v1 = v3-2;
        v2 = v3-1;
        v4 = v3+1;
        
        if( v1 < 0 )
          v1=0;
        if( v2 < 0 )
          v2=0;
        if( m_Moves.size() <= v3 )
          v3=m_Moves.size()-1;
        if( m_Moves.size() <= v4 )
          v4=m_Moves.size()-1;		
        
        if( t != 1.0f )  // if we need to calculate a new t, due to multiple moves per turn
        {
          t = (time - m_Moves[v3].start) / (m_Moves[v3].end - m_Moves[v3].start);
        }
        
        t = pow(t, (2.0f/3.0f)); // to ease into thier final positions make t = t^(2/3)
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
        
        if( selected )
        {
          //MoveInfo();
          //cout << "at time: " << time << " decided on v3 of " << v3 << " for ship id " << id << " of owner " << owner << " that is at (" << m_Moves[v3].point.x << "," << m_Moves[v3].point.y << ") from " << m_Moves[v3].start << " to " << m_Moves[v3].end << " and calc (" << px << "," << py << ")" << endl;
        }
        return make_pair( SpacePoint( px, py ), atan2( hy, hx ) );
      }
      
  };
}

#endif  // PERSISTENTS
