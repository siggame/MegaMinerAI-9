#include "space.h"
#include "spaceAnimatable.h"
#include "frame.h"
#include "animations.h"

namespace visualizer
{

  Space::Space()
  {
  } // Space::Space()

  Space::~Space()
  {
  } // Space::~Space()

  PluginInfo Space::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "Space";
    i.returnFilename = false;
    i.spectateMode = true;
    i.pluginName = "MegaMinerAI9: Space Plugin";

    options->loadOptionFile( "./plugins/space/space.xml", "space" );

    return i;
  } // PluginInfo Space::getPluginInfo()

  void Space::setup()
  {
    
    /*renderer->setCamera( 0, 0, 8, 8 );
    renderer->setGridDimensions( 8, 8 );
    
    resourceManager->loadResourceFile( "./plugins/space/textures.r" );

    animationEngine->registerGame( this, this ); */
  }

  void Space::loadGamelog( std::string gamelog )
  {
    // BEGIN: Initial Setup
    cout << "Load Space Gamelog" << endl;

    setup();

    m_game = new parser::Game;
    
    cout << "done setting up" << endl;
    
    if( !parser::parseGameFromString( *m_game, gamelog.c_str() ) )
    {
        cout << "in if\n";
      delete m_game;
      m_game = 0;
      errorLog << gamelog;
      THROW
        (
        GameException,
        "Cannot load gamelog, %s", 
        gamelog.c_str()
        );
        cout << "done in if\n";
    }
    // END: Initial Setup
    cout << "abotu to load()\n";
    load();
    cout << "abtou to return" << endl;
    return;
  } // Space::loadGamelog()

  void Space::load()
  {
    // Setup the renderer as mapRadius*2 x mapRadius*2
    renderer->setCamera( 0, 0, m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2);
    renderer->setGridDimensions( m_game->states[0].mapRadius * 2, m_game->states[0].mapRadius * 2 );
    resourceManager->loadResourceFile( "./plugins/space/textures.r" );
    animationEngine->registerGame( this, this );    
    
    timeManager->setNumTurns( m_game->states.size() );
    
    // Loop through each state in the gamelog
    for(int state = 0; state < m_game->states.size(); state++)
    {
        Frame turn;
        cout << m_game->states[ state ].mapRadius << endl;
        
        // Add and draw the background
        SmartPointer<Background> background = new Background();
        background->addKeyFrame( new DrawBackground() );
        turn.addAnimatable( background );
        
        /*// Loop though each Piece in the current state
        for(std::map<int, parser::Piece>::iterator i = m_game->states[ state ].pieces.begin(); i != m_game->states[ state ].pieces.end(); i++)
        {
            SmartPointer<SpacePiece> piece = new SpacePiece();
            
            piece->x = i->second.file - 1;
            piece->y = i->second.rank - 1;
            piece->type = i->second.type;
            piece->owner = i->second.owner;
            
            piece->addKeyFrame( new DrawSpacePiece( piece ) );
            turn.addAnimatable( piece );
        }*/
        addFrame( turn );
    }
    
    timeManager->play();
  }

} // visualizer

Q_EXPORT_PLUGIN2( Space, visualizer::Space );
