#ifndef PERSISTENTS_H
#define PERSISTENTS_H
#include "parser/structures.h"
#include <vector>
#include <math.h>
#include <map>
#include <utility>
#include <sstream>
#include "glm/glm.hpp"

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
        m_X = ship.x;
        m_Y = ship.y;
        m_Round = round;
        selected = false;

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
        return ( turn >= createdAtTurn && turn < createdAtTurn + (int)healths.size() && (m_Round == round || round == -1) );
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

      float StealthOn( int /*turn*/, float /*t*/)
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

        for(int i = 0; i < (signed)m_Moves.size(); i++)
        {
          //cout << id << ": #" << i << ":  (" << m_Moves[i].point.x << "," << m_Moves[i].point.y << ") @" << m_Moves[i].start << " to " << m_Moves[i].end << endl;
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
          pts << "(" << points[turn].x << "," << points[turn].y << ")";
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

        //cout << m0 << m1 << endl;

        glm::vec4 m = times * glm::transpose(A);

        glm::vec2 result = q * m;


#if 0
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
#endif

        return make_pair( SpacePoint( result.x, result.y ), 0 );
      }

  };
}

#endif  // PERSISTENTS
