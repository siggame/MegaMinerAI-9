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
        game->renderer->drawLine(490, 500, 510, 500, 1);
        game->renderer->drawLine(500, 490, 500, 510, 1);
        game->renderer->drawCircle(500, 500, 500, 1);
    }
  
    void DrawSpaceShip::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
        Color teamColor[] = { Color(0.666, 0, 0), Color(0, 0, 0.666) };
        
        SpaceShip &ship = *m_spaceShip;
        
                // Build the ship type string and replace spaces with '-'
        string shipType = ship.type;
        for(int i = 0; i < shipType.length(); i++)
        {
            if(shipType[i] == ' ')
            {
                shipType[i] = '-';
            }
        }
        
        
        game->renderer->setColor( Color(1, 1, 1) );
        
        //if( game->options->getNumber( "RotateBoard" ) )
        game->renderer->drawTexturedQuad((float)ship.x - (float)ship.radius, (float)ship.y - (float)ship.radius, ship.radius * 2, ship.radius * 2, shipType);
        game->renderer->setColor( teamColor[ship.owner] );
        game->renderer->drawCircle(ship.x, ship.y, ship.radius, 1);
    }

}
