#include "space.h"
#include "spaceAnimatable.h"
#include "frame.h"
#include "version.h"
#include "animations.h"
#include "persistents.h"

namespace visualizer
{
  Space::Space()
  {
    m_game = 0;
  } // Space::Space()

  Space::~Space()
  {
    destroy();
  }

  void Space::destroy()
  {
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
    //cout << "PRE" << endl;
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

  }

  list<int> Space::getSelectedUnits()
  {
    list< int > selectedShipIDs;

    for ( auto& i : m_PersistentShips )
    {
      selectedShipIDs.push_back( i.second->id );
    }
    return selectedShipIDs;
  }

  void Space::loadGamelog( std::string gamelog )
  {
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

    load();
    return;
  } // Space::loadGamelog()

  void Space::load()
  {
    map < int, vector< SmartPointer < Warp > > > Warps;
    Warps[ -1 ] = vector< SmartPointer< Warp > >();

    // Setup the renderer as mapRadius*2 x mapRadius*2
    renderer->setCamera( 0, 0, m_game->states[0].outerMapRadius * 2, m_game->states[0].outerMapRadius * 2);
    renderer->setGridDimensions( m_game->states[0].outerMapRadius * 2, m_game->states[0].outerMapRadius * 2 );
    
    resourceManager->loadResourceFile( "./plugins/space/resources.r" );
    
    // Build the Debug Table's Headers
    QStringList header;
    header << "Owner" << "Type" << "Locations" << "Health" << "Attacks";
    gui->setDebugHeader( header );

    int p = programs["test"] = renderer->createShaderProgram();
    renderer->attachShader( p, "testShader" );
    renderer->buildShaderProgram( p );

    p = programs["post"] = renderer->createShaderProgram();
    renderer->attachShader( p, "post1" );
    renderer->buildShaderProgram( p );

    animationEngine->registerGame( this, this );

    m_outerMapRadius = m_game->states[ 0 ].outerMapRadius;
    m_innerMapRadius = m_game->states[ 0 ].innerMapRadius;

    timeManager->setNumTurns( m_game->states.size() );

    // BEGIN: Look through the game logs and build the m_PersistentShips
    for(int state = 0; state < (int)m_game->states.size(); state++)
    {
      Warps[ state ] = vector< SmartPointer< Warp > >();
      // Loop though each PersistentShip in the current state
      for(auto& i : m_game->states[ state ].ships)
      {
        int shipID = i.second.id;

        // If the current ship's ID does not map to a PersistentShip in the map, create it and the warp for it
        if( m_PersistentShips.find(shipID) == m_PersistentShips.end() )
        {
          m_PersistentShips[shipID] = new PersistentShip(state, m_game->states[ state ].round, i.second);

          // Add the warps for this ship (so long as it is not a mine)
          if( strcmp( i.second.type, "Mine" ) != 0)
          {
            Warps[ state - 1 ].push_back( new Warp( i.second.x + m_outerMapRadius, i.second.y + m_outerMapRadius, i.second.radius, i.second.owner, false ) );
            Warps[ state ].push_back( new Warp( i.second.x + m_outerMapRadius, i.second.y + m_outerMapRadius, i.second.radius, i.second.owner, true ) );
          }
        }


        // Now the current ship we are looking at for sure exists as a PersistentShip, so fill it's values for this turn
        m_PersistentShips[shipID]->points.push_back( SpacePoint( i.second.x, i.second.y ) );
        m_PersistentShips[shipID]->healths.push_back( i.second.health );
        m_PersistentShips[shipID]->emps.push_back( false );
        
        vector< SpacePoint > moves;
        // Check for this ship's animations in the gamelog
        for( auto& j : m_game->states[state].animations[shipID] )
        {
          switch( j->type )
          {
            case parser::MOVE:
            {
                parser::move &move = (parser::move&)*j;
                if( !m_PersistentShips[shipID]->HasMoves() )
                {
                    moves.push_back( SpacePoint( move.fromX, move.fromY ) );
                }
                moves.push_back( SpacePoint( move.toX, move.toY ) );
            } break;
            case parser::ATTACK:
              {
                parser::attack &attack = (parser::attack&)*j;
                m_PersistentShips[shipID]->AddAttack( m_PersistentShips[m_game->states[ state - 1 ].ships[ attack.targetID ].id], state );

              } break;
            case parser::STEALTH:
              {
                m_PersistentShips[shipID]->AddStealth( state );
              }
            case parser::DESTEALTH:
              {
                m_PersistentShips[shipID]->AddDeStealth( state );
              }
          }
        }
        
        m_PersistentShips[shipID]->AddTurn( state, moves );
      }
    }

    for ( auto& i : m_PersistentShips )
    {
      i.second->Finalize();
    }
    // END: Look through the game logs and build the m_PersistentShips



    // BEGIN: Add every draw animation
    for(int state = 0; state < (int)m_game->states.size(); state++)
    {
      Frame turn;  // The frame that will be drawn

      // Add and draw the background
      SmartPointer<Background> background = new Background();
      background->outerRadius = m_outerMapRadius;
      background->innerRadius = m_innerMapRadius;
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
          dto.str("");
          dto << i.second->HealthOn(state, 0) << "/" << i.second->maxHealth;
          turn[i.first]["Health"] = dto.str().c_str();
          dto.str("");
          turn[i.first]["Attacks"] = i.second->AttacksWhoOn( state ).c_str();

          // Then and and draw it
          SmartPointer<PersistentShipAnim> ship = new PersistentShipAnim();
          ship->addKeyFrame( new DrawPersistentShip( i.second, state, &m_outerMapRadius ) );
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
        SmartPointer<RoundHUD> roundHUD = new RoundHUD( m_game->states[ state ].round, m_game->states[ state ].turnNumber, roundWinnerID == -1 ? "Draw" : m_game->states[0].players[ roundWinnerID ].playerName, roundWinnerID, m_outerMapRadius, state+1 == m_game->states.size() || m_game->states[ state ].round < m_game->states[ state + 1 ].round );
        roundHUD->addKeyFrame( new DrawRoundHUD( roundHUD ) );
        turn.addAnimatable( roundHUD );

      addFrame( turn );
    }
    // END: Add every draw animation

    timeManager->play();
  }

} // visualizer

Q_EXPORT_PLUGIN2( Space, visualizer::Space );
