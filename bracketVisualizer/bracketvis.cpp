#include <utility>
#include <time.h>
#include <list>
#include <QDomDocument>
#include <QFile>
#include "bracketvis.h"

namespace visualizer
{
  BracketVis::BracketVis()
  {
  } 

  BracketVis::~BracketVis()
  {
    destroy();
  }

  void BracketVis::destroy()
  {
  } 

  void BracketVis::preDraw()
  {
  }

  void BracketVis::postDraw()
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


  PluginInfo BracketVis::getPluginInfo()
  {
    PluginInfo i;
    i.searchLength = 1000;
    i.gamelogRegexPattern = "<response>";
    i.returnFilename = true;
    i.spectateMode = false;
    i.pluginName = "MegaMinerAI Bracket Visualizer";

    return i;
  } 

  void BracketVis::loadGamelog( std::string gamelog )
  {
    QDomDocument doc( "TournamentML" );
    QFile file( gamelog.c_str() );

    if( !file.open( QIODevice::ReadOnly ) )
    {
      WARNING( "Could not load tournament file: %s", gamelog.c_str() );
      return;
    }

    if( !doc.setContent( &file ) )
    {
      file.close();
      WARNING( "%s was unable to parse the XML", gamelog.c_str() );
      return;
    }

    file.close();

    QDomElement root = doc.documentElement().firstChild().toElement();

    if( root.tagName() != "objects" )
    {
      WARNING( "%s did not have an 'objects' root.", gamelog.c_str() );
      return;
    }

    QDomElement n = root.firstChild();
    while( !n.isNull() )
    {
      QDomElement e = n.toElement();
      if( !e.isNull() )
      {

      }

    }
  } 

} // visualizer

Q_EXPORT_PLUGIN2( BracketVis, visualizer::BracketVis );
