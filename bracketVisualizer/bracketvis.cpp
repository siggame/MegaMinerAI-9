#include <utility>
#include <time.h>
#include <list>
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
    i.gamelogRegexPattern = "Space";
    i.returnFilename = false;
    i.spectateMode = true;
    i.pluginName = "MegaMinerAI9: Space Plugin";


    return i;
  } 

  void BracketVis::loadGamelog( std::string gamelog )
  {
  } 

} // visualizer

Q_EXPORT_PLUGIN2( BracketVis, visualizer::BracketVis );
