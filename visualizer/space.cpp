#include "space.h"
#include "spaceAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include "persistents.h"
#include <utility>

namespace visualizer
{
  bool intersects( SpacePoint selectionA, SpacePoint selectionB, SpacePoint shipA, SpacePoint shipB )
  {
    if (selectionB.y < shipA.y) return(false);
    if (selectionA.y > shipB.y) return(false);

    if (selectionB.x < shipA.x) return(false);
    if (selectionA.x > shipB.x) return(false);
    
    return true;
  }  

  Space::Space()
  {
    m_game = 0;
    m_suicide=false;
  } // Space::Space()

  Space::~Space()
  {
    destroy();
  }

  void Space::destroy()
  {
    m_suicide=true;
    wait();
    animationEngine->registerGame(0, 0);

    clear();
    delete m_game;
    m_game = 0;

    // free up all the memory from the PersistentShips
    for ( auto& i : m_PersistentShips )
    {
      delete i.second;
    }

    m_PersistentShips.clear();
    programs.clear();

  } // Space::~Space()

  void Space::preDraw()
  {
    const Input& input = gui->getInput();
    if( input.leftRelease )
    {
      int turn = timeManager->getTurn();
      float t = timeManager->getTurnPercent();
      int x = input.x - m_mapRadius,
          sx = input.sx - m_mapRadius, 
          y = input.y - m_mapRadius, 
          sy = input.sy - m_mapRadius;
      //int x = input.x, sx = input.sx, y = input.y, sy = input.sy;
      for ( auto& i : m_PersistentShips )
      {
        if( i.second->ExistsAtTurn( turn, -1 ) )
        {
          // rough rectangle selection
          auto loc = i.second->LocationOn( turn, t );
          SpacePoint selectionA, selectionB;
          SpacePoint shipA = SpacePoint( float(loc.x - 0.75f*i.second->radius), float(loc.y - 0.75f*i.second->radius) );
          SpacePoint shipB = SpacePoint( float(loc.x + 0.75f*i.second->radius), float(loc.y + 0.75f*i.second->radius) );
          
          selectionA.x = x < sx ? x : sx;
          selectionA.y = y < sy ? y : sy;
          selectionB.x = x > sx ? x : sx;
          selectionB.y = y > sy ? y : sy;

          i.second->selected = intersects( selectionA, selectionB, shipA, shipB );
        }
      }
    }
  }

  void Space::postDraw()
  {
    if( renderer->fboSupport() )
    {
#if 0
      renderer->useShader( programs["post"] ); 
      renderer->swapFBO();
      renderer->useShader( 0 );
#endif

    }
  }


  PluginInfo Space::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "Space";
    i.returnFilename = false;
    i.spectateMode = true;
    i.pluginName = "MegaMinerAI9: Space Plugin";


    return i;
  } // PluginInfo Space::getPluginInfo()

  void Space::setup()
  {
    gui->checkForUpdate( "Space", "./plugins/space/checkList.md5", VERSION_FILE );
    options->loadOptionFile( "./plugins/space/space.xml", "space" );
    resourceManager->loadResourceFile( "./plugins/space/resources.r" );

    int p = programs["test"] = renderer->createShaderProgram();
    renderer->attachShader( p, "testShader" );
    renderer->buildShaderProgram( p );

    p = programs["post"] = renderer->createShaderProgram();
    renderer->attachShader( p, "post1" );
    renderer->buildShaderProgram( p );

  }
  

  list<int> Space::getSelectedUnits()
  {
    list< int > selectedShipIDs;

    for ( auto& i : m_PersistentShips )
    {
      if( i.second->selected )
      {
        selectedShipIDs.push_back( i.second->id );
      }
    }
    return selectedShipIDs;
  }

  void Space::loadGamelog( std::string gamelog )
  {
    if(isRunning())
    {
      m_suicide = true;
      wait();
    }
    m_suicide = false;

    // BEGIN: Initial Setup
    setup();

    delete m_game;
    m_game = new parser::Game;

    if( !parser::parseGameFromString( *m_game, gamelog.c_str() ) )
    {
      delete m_game;
      m_game = 0;
      WARNING(
          "Cannot load gamelog, %s", 
          gamelog.c_str()
          );
    }
    // END: Initial Setup
    
    // Setup the renderer as mapRadius*2 x mapRadius*2
    renderer->setCamera( 0, 0, m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2);
    renderer->setGridDimensions( m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2 );
 
    start();
  } // Space::loadGamelog()

  void Space::run()
  {
    map < int, vector< SmartPointer < Warp > > > Warps;
    Warps[ 0 ] = vector< SmartPointer< Warp > >();
    
    // Build the Debug Table's Headers
    QStringList header;
    header << "Owner" << "Type" << "Locations" << "Movement Left" << "Health" << "Attacks Who";
    gui->setDebugHeader( header );

    animationEngine->registerGame(0, 0);

    m_mapRadius = m_game->states[ 0 ].mapRadius;

    timeManager->setNumTurns( 0 );

    // BEGIN: Look through the game logs and build the m_PersistentShips
    for(int state = 0; state < (int)m_game->states.size() && !m_suicide; state++)
    {
      Warps[ state+1 ] = vector< SmartPointer< Warp > >();
      
      // Find all the ships we need to look at this turn
      vector< pair<int, parser::Ship> > ships;
      
      // Loop though each PersistentShip in the current state, and them to the shipIDs to look at
      for(auto& i : m_game->states[ state ].ships)
      {
        i.second.y *= -1;
        pair< int, parser::Ship > p;
        p.first = i.first;
        p.second = i.second;
        ships.push_back( p );
      }
      
      // 
      if( state >= 2 )
      {
        for(auto& ship : m_game->states[ state - 2 ].ships)
        {
          bool existsInCurrentShips = false;
          for( auto& currentShip : ships )
          {
            if( currentShip.first == ship.first )
            {
              existsInCurrentShips = true;
              break;
            }
          }
          
          if( !existsInCurrentShips )
          {
            pair< int, parser::Ship > p;
            p.first = ship.first;
            p.second = ship.second;
            
            p.second.health = 0;
            
            ships.push_back( p );
          }
        }
      }
      
      for( auto& i : ships )
      {
        int shipID = i.second.id;

        // If the current ship's ID does not map to a PersistentShip in the map, create it and the warp for it
        if( m_PersistentShips.find(shipID) == m_PersistentShips.end() )
        {
          m_PersistentShips[shipID] = new PersistentShip(state, m_game->states[ state ].round, i.second);

          // Add the warps for this ship (so long as it is not a mine)
          if( strcmp( i.second.type, "Mine" ) != 0)
          {
            Warps[ state ].push_back( new Warp( i.second.x + m_mapRadius, i.second.y + m_mapRadius, i.second.radius, i.second.owner, false ) );
            Warps[ state+1 ].push_back( new Warp( i.second.x + m_mapRadius, i.second.y + m_mapRadius, i.second.radius, i.second.owner, true ) );
          }
        }

        vector< SpacePoint > moves;
        
        // Check for this ship's animations in the gamelog
        for( auto& j : m_game->states[state].animations[shipID] )
        {
          switch( j->type )
          {
            case parser::MOVE:
            {
              parser::move &move = (parser::move&)*j;
              if( !m_PersistentShips[shipID]->HasMoves()  )
              {
                  moves.push_back( SpacePoint( move.fromX, -move.fromY ) );
              }
              moves.push_back( SpacePoint( move.toX, -move.toY ) );
              //if( shipID == 37 )
                //cout << "Move found on turn " << state << " with ship id " << shipID << " of owner " << m_PersistentShips[shipID]->owner << " moving from (" << move.fromX << "," << move.fromY << ") to (" << move.toX << "," << move.toY << ")" << endl;
            } break;
            case parser::ATTACK:
            {
              parser::attack &attack = (parser::attack&)*j;
              m_PersistentShips[shipID]->AddAttack( m_PersistentShips[ attack.targetID ], state );
              
              // If this is an EMP attack we need to EMP the victim
              if( strcmp( "EMP", m_PersistentShips[shipID]->type.c_str() ) == 0 )
              {
                m_PersistentShips[ attack.targetID ]->AddEMPed( state + 1 );
              }
              
              //if( shipID == 10 )
                //cout << "Attack found on turn " << state << " of attacker " << shipID << " attacking " << attack.targetID << endl;
              
            } break;
            case parser::STEALTH:
            {
              m_PersistentShips[shipID]->AddStealth( state );
            } break;
            case parser::DESTEALTH:
            {
              m_PersistentShips[shipID]->AddDeStealth( state );
            } break;
            case parser::SELFDESTRUCT:
            {
              m_PersistentShips[shipID]->SelfDestructs = true;
            } break;
          }
        }
        
        if( !m_PersistentShips[shipID]->HasMoves() && state == m_PersistentShips[shipID]->FirstTurn() )
        {
          moves.push_back( SpacePoint( i.second.x, i.second.y ) );
        }
        
        m_PersistentShips[shipID]->AddTurn( state, moves, i.second.health, i.second.movementLeft );
        
        // Check to see if this ship dies next turn (doesn't exist next turn)
        if( state + 1 != m_game->states.size() )
        {
          if( m_game->states[ state + 1 ].ships.find( shipID ) == m_game->states[ state + 1 ].ships.end() )
          {
            m_PersistentShips[shipID]->AddDeath( state + 1 );
          }
        }
      }
      
      //////////////////////////////////////////////////////////////////////////
      // Start adding stuff to draw
      Frame turn;  // The frame that will be drawn

      // Add and draw the background
      SmartPointer<Background> background = new Background();
      background->radius = m_mapRadius;
      background->turn = m_game->states[ state ].turnNumber;
      background->addKeyFrame( new DrawBackground( background ) );
      turn.addAnimatable( background );

      // Add each Warp to be drawn
      for(unsigned int i = 0; i < Warps[ state ].size(); i++)
      {
        SmartPointer<Warp> warp = new Warp( *Warps[ state ][ i ] );
        warp->addKeyFrame( new DrawWarp( warp ) );
        turn.addAnimatable( warp );
      }

      // Add each players information to the HUD and draw it
      for(int playerid = 0; playerid < 2; playerid++)
      {
        SmartPointer<PlayerHUD> hud = new PlayerHUD( m_game->states[state].players[playerid], (m_game->winner == playerid) );
        hud->addKeyFrame( new DrawPlayerHUD(hud) );
        turn.addAnimatable( hud );
      }
        
      // For each of our PersistentShips
      for( auto& i : m_PersistentShips )
      {
        // If it exists
        if(i.second->ExistsAtTurn( state, m_game->states[ state ].round ))
        {
          stringstream dto; // debug table output
          turn[i.first]["Owner"] = i.second->owner; 
          turn[i.first]["Type"] = i.second->type.c_str();
          turn[i.first]["Locations"] = i.second->PointsOn( state ).c_str();
          turn[i.first]["Movement Left"] = i.second->MovementOn( state ).c_str();
          dto.str("");
          dto << i.second->HealthOn(state, 0) << "/" << i.second->maxHealth;
          turn[i.first]["Health"] = dto.str().c_str();
          dto.str("");
          turn[i.first]["Attacks Who"] = i.second->AttacksWhoOn( state ).c_str();

          // Then and and draw it
          SmartPointer<PersistentShipAnim> ship = new PersistentShipAnim();
          ship->addKeyFrame( new DrawPersistentShip( i.second, state, &m_mapRadius ) );
          turn.addAnimatable( ship );
        }
      }
      
      // Add the RoundHUD
      int roundWinnerID = -1;
      if( m_game->states.size() == state+1 )
      {
        roundWinnerID = m_game->winner;
      }
      else
      {
        if( m_game->states[ state + 1 ].players[0].victories > m_game->states[ state ].players[0].victories )
        {
          roundWinnerID = 0;
        }
        if( m_game->states[ state + 1 ].players[1].victories > m_game->states[ state ].players[1].victories )
        {
          if( roundWinnerID == 0 )
          {
            roundWinnerID = -1;
          }
          else
          {
            roundWinnerID = 1;
          }
        }
      }
      
      // Get all the ship types for this round
      vector< char* > shipTypes;
      for( auto& shipType : m_game->states[ state ].shipTypes )
      {
        shipTypes.push_back( shipType.second.type );
      }
      
      SmartPointer<RoundHUD> roundHUD = new RoundHUD( m_game->states[ state ].round, m_game->states[ state ].turnNumber, roundWinnerID == -1 ? "Draw" : m_game->states[0].players[ roundWinnerID ].playerName, roundWinnerID, m_mapRadius, state+1 == m_game->states.size() || m_game->states[ state ].round < m_game->states[ state + 1 ].round, shipTypes );
      roundHUD->addKeyFrame( new DrawRoundHUD( roundHUD ) );
      turn.addAnimatable( roundHUD );

      animationEngine->buildAnimations(turn);
      addFrame(turn);
      if(state > 5)
      {
        timeManager->setNumTurns(state - 5);
        if(state == 6)
        {
          animationEngine->registerGame(this, this);
          timeManager->setTurn(0);
          timeManager->play();
        }
      }
    }
    // END: Add every draw animation

    if(!m_suicide)
    {
      // Just make sure the game is registered correctly
      animationEngine->registerGame(this, this);
    }

    for(auto& i : m_PersistentShips)
    {
      if( m_suicide )
        break;
    }

    // END: Look through the game logs and build the m_PersistentShips

    if(!m_suicide)
    {
      timeManager->setNumTurns( m_game->states.size() );
      timeManager->play();
    }

  }

} // visualizer

Q_EXPORT_PLUGIN2( Space, visualizer::Space );
