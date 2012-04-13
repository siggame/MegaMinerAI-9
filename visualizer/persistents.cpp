#include "persistents.h"

namespace visualizer
{


  ostream& operator <<( ostream& os, const glm::vec2& v )
  {
    os << "(" << v.x << ", " << v.y << ")";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::vec4& v )
  {
    os << "(" << v.x << ", " << v.y << ", " << v.z << ", " << v.w << ")";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::mat4x2& m )
  {

    os << "[" << m[0] << ", " << endl;
    os << m[1] << endl;
    os << m[2] << endl;
    os << m[3] << "]";
    return os;
  }

  ostream& operator <<( ostream& os, const glm::mat4& m )
  {
    os << "[" << m[0] << ", " << endl;
    os << m[1] << endl;
    os << m[2] << endl;
    os << m[3] << "]";
    return os;
  }

  PersistentShip::PersistentShip(int createdAt, int round, parser::Ship ship)
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

  void PersistentShip::AddTurn(int turn, vector<vec2> &moves, int health, int movementLeft, int attacksLeft)
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
        if(m_Moves.back().point.x == move.point.x && m_Moves.back().point.y == move.point.y)
        {
          
        }
        else
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
  
  bool PersistentShip::HasMoves() { return m_Moves.size() > 0; }

  bool PersistentShip::ExistsAtTurn(int turn, int round)
  {
    return ( turn >= m_CreatedAtTurn && turn <= m_DeathTurn && (m_Round == round || round == -1) );
  }

  vec2 PersistentShip::LocationOn(int turn, float t)
  {
    auto lah = SplineOn(turn, t);
    return lah.first;
  }

  float PersistentShip::HeadingOn(int turn, float t)
  {
    auto lah = SplineOn(turn, t);
    return lah.second;
  }

  float PersistentShip::HealthOn(int turn, float t)
  {
    turn -= m_CreatedAtTurn;

    // h(t) = a + t(b - a)
    return m_Healths[PreviousTurn(turn)] + t * ( m_Healths[turn] - m_Healths[PreviousTurn(turn)] );
  }

  bool PersistentShip::EMPedOn(int turn)
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

  vector<vec2> PersistentShip::AttacksOn( int turn, float t )
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

  void PersistentShip::AddAttack( PersistentShip* victim, int turn )
  {
    if(m_AttackVictims.find( turn ) == m_AttackVictims.end())
    {
      m_AttackVictims[turn] = vector< PersistentShip* >(); 
    }

    m_AttackVictims[turn].push_back( victim );
  }

  void PersistentShip::AddStealth( int turn )
  {
    m_Stealths.push_back( pair<int,char>(turn, 's') );
  }

  void PersistentShip::AddDeStealth( int turn )
  {
    m_Stealths.push_back( pair<int,char>(turn, 'd') );
  }

  void PersistentShip::AddEMPed( int turn )
  {
    m_EMPeds.push_back( turn );
  }

  float PersistentShip::StealthOn( int /*turn*/, float /*t*/)
  {
    return (strcmp("Stealth", type.c_str()) != 0) ? 1 : 0.3f;
  }

  float PersistentShip::ExplodingOn( int turn )
  {
    return turn == m_DeathTurn;
  }

  bool PersistentShip::RenderShield()
  {
    return !(strcmp( "Mine", type.c_str() ) == 0);
  }

  bool PersistentShip::RenderRange()
  {
    return (strcmp( "Mine", type.c_str() ) == 0) || (strcmp( "Support", type.c_str() ) == 0);
  }

  string PersistentShip::PointsOn( int turn )
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

  string PersistentShip::AttacksWhoOn( int turn )
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

  string PersistentShip::MovementOn( int turn )
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

  void PersistentShip::AddDeath( int turn )
  {
    m_DeathTurn = turn;
    m_Healths.push_back( 0 );
  }
      
  void PersistentShip::MoveInfo()
  {
    return;
    
    cout << "Ship " << id << " of type " << type << endl;
    for( auto& move : m_Moves )
    {
      cout << "  (" << move.point.x << "," << move.point.y << ") from " << move.start << " to " << move.end << endl;
    }
  }
      
  pair<vec2, float> PersistentShip::SplineOn(int turn, float t)
  {
    int v1, v2, v3, v4;
    v1 = v2 = v3 = v4 = -1;
    bool foundV3 = false;

    float time = float(turn) + t;
    if(m_Moves.size() == 0)
      return make_pair( vec2( m_InitialX, m_InitialY ), 0 );
    
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

    return make_pair(vec2(px, py), atan2(hy, hx));
  }
} // visualizer
