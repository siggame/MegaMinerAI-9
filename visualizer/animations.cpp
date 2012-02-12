#include "animations.h"
#include "space.h"
#include <sstream>

namespace visualizer
{
    void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
    }

    void DrawBackground::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
        game->renderer->setColor( Color( 1, 1, 1 ) );
        game->renderer->drawTexturedQuad(0, 0, 2000, 2000, "background");
        game->renderer->drawCircle(1000, 1000, 1000, 1);
    }
  
    void DrawSpacePiece::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
        SpacePiece &piece = *m_piece;

        stringstream ss;

        ss << 1-piece.owner << "-" << (char)piece.type;

        game->renderer->setColor( Color( 1, 1, 1 ) );
        if( game->options->getNumber( "RotateBoard" ) )
          game->renderer->drawTexturedQuad(7-piece.x, piece.y, 1, 1, ss.str());
        else
          game->renderer->drawTexturedQuad(piece.x, 7-piece.y, 1, 1, ss.str());

    }

}
