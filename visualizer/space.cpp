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
    } // Space::Space()

    Space::~Space()
    {
        // free up all the memory from the PersistentShips
        for (std::map< int, PersistentShip* >::iterator iter = m_PersistentShips.begin(); iter != m_PersistentShips.end(); ++iter)
        {
            delete iter->second;
        }
        
    } // Space::~Space()

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
        /*renderer->setCamera( 0, 0, 8, 8 );
          renderer->setGridDimensions( 8, 8 );

          resourceManager->loadResourceFile( "./plugins/space/textures.r" );

          animationEngine->registerGame( this, this ); */
    }

  void Space::loadGamelog( std::string gamelog )
  {
    // BEGIN: Initial Setup
    setup();

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
    // Setup the renderer as mapRadius*2 x mapRadius*2
    renderer->setCamera( 0, 0, m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2);
    renderer->setGridDimensions( m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2 );
    resourceManager->loadResourceFile( "./plugins/space/textures.r" );

    int p = programs["test"] = renderer->createShaderProgram();
    renderer->attachShader( p, "testShader" );
    renderer->buildShaderProgram( p );

    animationEngine->registerGame( this, this );

    m_mapRadius =  m_game->states[ 0 ].mapRadius;
    m_MapRadius = new int();
    *m_MapRadius = m_mapRadius = m_game->states[ 0 ].mapRadius;;

    timeManager->setNumTurns( m_game->states.size() );
    
    for(int state = 0; state < m_game->states.size(); state++)
    {
      continue;  // because fuck the PO LISE (aka Gardner)
      Frame turn;

      // Add and draw the background
      SmartPointer<Background> background = new Background();
      background->addKeyFrame( new DrawBackground() );
      turn.addAnimatable( background );

      // Loop though each Ship in the current state
      for(std::map<int, parser::Ship>::iterator i = m_game->states[ state ].ships.begin(); i != m_game->states[ state ].ships.end(); i++)
      {
        SmartPointer<SpaceShip> ship = new SpaceShip();

        ship->id = i->second.id;
        ship->owner = i->second.owner;
        ship->y = i->second.y + m_mapRadius;
        ship->x = i->second.x + m_mapRadius;
        ship->health = i->second.health;
        ship->maxHealth = i->second.maxHealth;
        ship->radius = i->second.radius;

        turn[ship->id]["x"] = ship->x;
        turn[ship->id]["y"] = ship->y;
        turn[ship->id]["radius"] = ship->radius;

        if(i->second.type != NULL)
        {
          ship->type = i->second.type;
        }
        else
        {
          ship->type = "ship";
          //WARNING( "null type encountered on ship!" );
          cout << "null type encountered on ship!\n";
        }

        // Check for this ship's animations
        for
        (
           std::vector< SmartPointer< parser::Animation > >::iterator j = m_game->states[ state ].animations[ ship->id ].begin();
           j != m_game->states[ state ].animations[ ship->id ].end();
           j++
        )
        {
            switch( (*j)->type )
            {
              case parser::ATTACK:
                {
                  parser::attack &a = (parser::attack&)*(*j);

                  SmartPointer<AttackData> attack = new AttackData();

                  attack->attackerTeam = ship->owner;
                  attack->attackerX = m_game->states[ state ].ships[ a.acting ].x + m_mapRadius;
                  attack->attackerY = m_game->states[ state ].ships[ a.acting ].y + m_mapRadius;
                  attack->victimX = m_game->states[ state ].ships[ a.target ].x + m_mapRadius;
                  attack->victimY = m_game->states[ state ].ships[ a.target ].y + m_mapRadius;

                  ship->addKeyFrame( new DrawShipAttack( attack ) );
                  turn.addAnimatable( attack );

                } break;
            }
        }

        ship->addKeyFrame( new DrawSpaceShip( ship ) );
        turn.addAnimatable( ship );
      }

      addFrame( turn );
    }
    
    // BEGIN: Look through the game logs and build the m_PersistentShips
    for(int state = 0; state < (int)m_game->states.size(); state++)
    {
        // Loop though each PersistentShip in the current state
        for(std::map<int, parser::Ship>::iterator i = m_game->states[ state ].ships.begin(); i != m_game->states[ state ].ships.end(); i++)
        {
            int shipID = i->second.id;
            
            // If the current ship's ID does not map to a PersistentShip in the map, create it
            if( m_PersistentShips.find(shipID) == m_PersistentShips.end() )
            {
                m_PersistentShips[shipID] = new PersistentShip(state, i->second);
            }
            
            // Now the current ship we are looking at for sure exists as a PersistentShip, so fill it's values for this turn
            m_PersistentShips[shipID]->points.push_back( SpacePoint( i->second.x, i->second.y ) );
            m_PersistentShips[shipID]->healths.push_back( i->second.health );
            
            // Check for this ship's animations in the gamelog
            for
            (
               std::vector< SmartPointer< parser::Animation > >::iterator j = m_game->states[ state ].animations[ shipID ].begin();
               j != m_game->states[ state ].animations[ shipID ].end();
               j++
            )
            {
                switch( (*j)->type )
                {
                    // Attack animation
                    case parser::ATTACK:
                    {
                        parser::attack &a = (parser::attack&)*(*j);

                        /*SmartPointer<AttackData> attack = new AttackData();

                        attack->attackerTeam = ship->owner;
                        attack->attackerX = m_game->states[ state ].ships[ a.acting ].x + m_mapRadius;
                        attack->attackerY = m_game->states[ state ].ships[ a.acting ].y + m_mapRadius;
                        attack->victimX = m_game->states[ state ].ships[ a.target ].x + m_mapRadius;
                        attack->victimY = m_game->states[ state ].ships[ a.target ].y + m_mapRadius;

                        ship->addKeyFrame( new DrawShipAttack( attack ) );
                        turn.addAnimatable( attack );*/
                        
                        m_PersistentShips[shipID]->AddAttack( m_game->states[ state ].ships[ a.target ], state );
                        
                    } break;
                }
            }
        }
    }
    // END: Look through the game logs and build the m_PersistentShips
    
    
     
    // BEGIN: Add every draw animation
    for(int state = 0; state < (int)m_game->states.size(); state++)
    {
        Frame turn;  // The frame that will be drawn
        
        // Add and draw the background
        SmartPointer<Background> background = new Background();
        background->addKeyFrame( new DrawBackground() );
        turn.addAnimatable( background );
        
        // For each of our PersistentShips
        for (std::map< int, PersistentShip* >::iterator iter = m_PersistentShips.begin(); iter != m_PersistentShips.end(); ++iter)
        {
            // If it exists
            if(iter->second->ExistsAtTurn(state))
            {
                // Then and and draw it
                SmartPointer<PersistentShipAnim> ship = new PersistentShipAnim();
                background->addKeyFrame( new DrawPersistentShip( iter->second, state, m_MapRadius ) );
                turn.addAnimatable( ship );
            }
        }
        
        addFrame( turn );
    }
    // END: Add every draw animation
    
    timeManager->play();
  }

} // visualizer

Q_EXPORT_PLUGIN2( Space, visualizer::Space );
