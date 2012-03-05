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
        game->renderer->drawArc(500, 500, 500, 50 );
    }
  
    void DrawSpaceShip::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
        // HOW TO USE OPTIONS: if( game->options->getNumber( "RotateBoard" ) )
        
        Color teamColor[] = { Color(0.666, 0, 0), Color(0, 0, 0.666) };
        Color health = Color(0, 0.666, 0);
        
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
        
        // Build the Ship's Texture string in textures.r
        stringstream shipTexture;
        if(strcmp("ship",shipType.c_str()) == 0)
        {
            shipTexture << "Ship-Default";
        }
        else
        {
            shipTexture << "Ship-" << (ship.owner ? "Blue-" : "Red-") << shipType;
        }
        
        
        // Health Calculations
        const float upAngle = -90;
        const float healthSection = 100;
        ship.maxHealth = ship.maxHealth ? ship.maxHealth : 1;
        float healthLeft = float(ship.health)/ship.maxHealth;
        float healthStart = upAngle-healthSection*healthLeft;
        float healthEnd   = upAngle+healthSection*healthLeft;
        cout << healthLeft << endl;

        // Set the color to white for drawing the ship
        game->renderer->setColor( Color(1, 1, 1, 1) );
        game->renderer->drawTexturedQuad((float)ship.x - (float)ship.radius/1.25f, (float)ship.y - (float)ship.radius/1.25f, ship.radius * 1.6f, ship.radius * 1.6f, shipTexture.str());
        game->renderer->drawTexturedQuad((float)ship.x - (float)ship.radius, (float)ship.y - (float)ship.radius, ship.radius * 2.38f, ship.radius * 2.38f, (ship.owner ? "Blue-Shield" : "Red-Shield"));
        
        // Set the color to the team color to draw the outline of the shield
        //game->renderer->setColor( teamColor[ship.owner] );
        //game->renderer->drawCircle(ship.x, ship.y, ship.radius, 1);
        
        game->renderer->drawLine(ship.x - 5, ship.y, ship.x + 5, ship.y, 1);
        game->renderer->drawLine(ship.x, ship.y - 5, ship.x, ship.y + 5, 1);
        
        // Draw their health
        game->renderer->setColor( teamColor[ship.owner] );
        game->renderer->drawArc(ship.x, ship.y, ship.radius, 100, healthEnd, healthStart+360 );
        game->renderer->setColor( health );
        game->renderer->useShader( ((Space*)game)->programs["test"] );
        game->renderer->drawArc(ship.x, ship.y, ship.radius, 100, healthStart, healthEnd );
        game->renderer->useShader( 0 );
    }
    

    void DrawShipAttack::animate( const float& t, AnimData *d, IGame* game )
    {
        Color teamColor[] = { Color(1, 0, 0, t), Color(0, 0, 1, t) };
        
        //cout << "time t: " << t << endl;
        
        //AttackData *attack = (AttackData*)d;
        AttackData &attack = *m_attackData;
        
        //cout << "attack: a(" << attack.attackerX << "," << attack.attackerY << ") to v(" << attack.victimX << "," << attack.victimY << ")" << endl;
        
        game->renderer->setColor( teamColor[attack.attackerTeam] );
        game->renderer->drawLine(attack.attackerX, attack.attackerY, attack.victimX, attack.victimY, 2); 
        
        //if( t > startTime && t < endTime )
        //else if ( t >= endTime )
    } // DrawShipAttack::animate()

}
