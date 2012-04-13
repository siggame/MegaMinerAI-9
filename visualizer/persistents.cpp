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

  void PersistentShip::AddTurn(int turn, vector<vec2> &moves, int movementLeft)
  {
    // Add the moves
    float span = 1.0f / float(moves.size());
    for(float i = 0; i < (float)moves.size(); i++)
    {
      SpaceMove move;
      move.point = moves[i];
      move.start = (float)turn + i * span;
      move.end = (float)turn + (i+1) * span;

      m_Moves.push_back( move );
    }
    
    // Add the movement left
    m_MovementLeft.push_back( movementLeft );
  }

  bool PersistentShip::ExistsAtTurn(int turn, int round)
  {
    return ( turn >= createdAtTurn && turn <= m_DeathTurn && (m_Round == round || round == -1) );
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
    turn -= createdAtTurn;

    // h(t) = a + t(b - a)
    return healths[PreviousTurn(turn)] + t * ( healths[turn] - healths[PreviousTurn(turn)] );
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
    return (strcmp( "Mine", type.c_str() ) == 0) || (strcmp( "Support", type.c_str() ) == 0) || (strcmp( "Warp Gate", type.c_str() ) == 0);
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

  void PersistentShip::AddDeath( int turn )
  {
    m_DeathTurn = turn;
    healths.push_back( 0 );
    
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
    int v2 = -1;
    bool foundV2 = false;
    float time = float(turn) + t;

    if(m_Moves.size() == 0)
      return make_pair(vec2( m_InitialX, m_InitialY ), 0);
    
    for(int i = 0; i < m_Moves.size(); i++)
    {
      if( m_Moves[i].InRange( time ) )
      {
        v2 = i;
        i = m_Moves.size();
        foundV2 = true;
      }
      else if( m_Moves[i].start > time )
      {
        v2 = i-1;
        t = 1.0f;
        i = m_Moves.size();
        foundV2 = true;
      }
      else if( m_Moves[i].end < time )
      {
        continue;
      }
      else
      {
        // TODO: Put this back when we find out 
        // what's wrong.
        //THROW(Exception, "Shouldn't Happen");
          // Shouldn't happen
      }
    }

    if( !foundV2 )
    {
      v2 = m_Moves.size()-1;
      t = 1.0f;
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
    
    if( t != 1.0f )  // if we need to calculate a new t, due to multiple moves per turn
    {
      t = (time - m_Moves[v2].start) / (m_Moves[v2].end - m_Moves[v2].start);
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

  pair<vec2, float> PersistentShip::GardnersSplineOn(int turn, float t)
  {
#if 0
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
#endif
  }

} // visualizer
