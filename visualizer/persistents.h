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
      bool SelfDestructs;
      vector< int > m_Healths;

      PersistentShip(int createdAt, int round, parser::Ship ship);
      void AddTurn(int turn, vector<vec2> &moves, int health, int movementLeft, int attacksLeft);
      bool HasMoves();
      bool ExistsAtTurn(int turn, int round);
      vec2 LocationOn(int turn, float t);
      float HeadingOn(int turn, float t);
      float HealthOn(int turn, float t);
      bool EMPedOn(int turn);
      vector<vec2> AttacksOn( int turn, float t );
      void AddAttack( PersistentShip* victim, int turn );
      void AddStealth( int turn );
      void AddDeStealth( int turn );
      void AddEMPed( int turn );
      float StealthOn( int /*turn*/, float /*t*/);
      float ExplodingOn( int turn );
      bool RenderShield();
      bool RenderRange();
      string PointsOn( int turn );
      string AttacksWhoOn( int turn );
      string MovementOn( int turn );
      void AddDeath( int turn );
      int FirstTurn() { return m_CreatedAtTurn; }
      void MoveInfo();
      string AttacksLeftOn( int turn );
      map<int, vec2> m_idPositions;

    private:
      int m_CreatedAtTurn;
      float m_InitialX;
      float m_InitialY;

      map< int, vector < PersistentShip* > > m_AttackVictims;
      vector< pair< int, char > > m_Stealths;  // int represents the turn, char 's' represents that it went into stealth, 'd' is destealth
      vector< SpaceMove > m_Moves;
      int m_Round;
      vector<int> m_MovementLeft;
      int m_DeathTurn;
      vector< int > m_EMPeds;
      vector< int > m_AttacksLeft;
      

      int PreviousTurn(int turn)
      {
        return (turn > 0 ? turn - 1 : 0);
      }

      pair<vec2, float> GardnersSplineOn(int turn, float t);
      pair<vec2, float> SplineOn(int turn, float t);

  };
}

#endif  // PERSISTENTS_H
