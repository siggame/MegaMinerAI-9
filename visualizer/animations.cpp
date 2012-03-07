#include "animations.h"
#include "space.h"
#include "persistents.h"
#include <sstream>

namespace visualizer
{
    void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
    }


    void DrawBackground::animate( const float& /* t */, AnimData * /* d */, IGame* game )
    {
      cout << "background" << endl;
        game->renderer->setColor( Color( 1, 1, 1, 1 ) );
        game->renderer->drawTexturedQuad(0, 0, 2000, 2000, "background");
        game->renderer->setColor( Color( 1, 1, 1, 0.4f ) );
        game->renderer->drawLine(490, 500, 510, 500, 1);
        game->renderer->drawLine(500, 490, 500, 510, 1);
        game->renderer->drawArc(500, 500, 500, 50 );
    }
  
    
    void drawRotatedTexturedQuad( IGame* game, float x, float y, float length, float degrees, string texture)
    {
        /*game->renderer->push();
       game->renderer->translate( 500, 500 );
       game->renderer->rotate( 45, 0, 0, 1 );
       game->renderer->drawQuad( -50, -50, 100, 100 );
       game->renderer->pop();*/
       
       game->renderer->push();
       game->renderer->translate( x + length/2, y + length/2 );
       game->renderer->rotate( degrees, 0, 0, 1 );
       game->renderer->drawTexturedQuad( -1 * length/2, -1 * length/2, length, length, texture );
       game->renderer->pop();
    }
    
    
    void DrawPersistentShip::animate( const float& t, AnimData * d, IGame* game )
    {
      cout << "SHIP" << endl;
        // BEGIN: Variables we will need
        int shipOwner = m_PersistentShip->owner;
        SpacePoint shipCenter = m_PersistentShip->LocationOn(m_Turn, t);
        shipCenter.x += *m_MapRadius;
        shipCenter.y += *m_MapRadius;
        float shipHeading = m_PersistentShip->HeadingOn(m_Turn, t) * 57.3f + 270;//(m_PersistentShip->HeadingOn(m_Turn, t) == 0 ? (shipOwner ? 90 : 270) : m_PersistentShip->HeadingOn(m_Turn, t) * 57.3f + 270);
        float shipStealth = m_PersistentShip->StealthOn(m_Turn, t);
        
        float shipRadius = m_PersistentShip->radius;
        bool shipIsExploding = m_PersistentShip->ExplodingOn(m_Turn);
        bool renderShield = m_PersistentShip->RenderShield();
        bool renderRange = m_PersistentShip->RenderRange();
        int shipRange = m_PersistentShip->range;
        
        vector< SpacePoint > shipAttacks = m_PersistentShip->AttacksOn( m_Turn, t );
        for(unsigned int i = 0; i < shipAttacks.size(); i++)
        {
            shipAttacks[i].x += *m_MapRadius;
            shipAttacks[i].y += *m_MapRadius;
        }
        
        string shipShieldTexture = (m_PersistentShip->owner ? "Blue-Shield" : "Red-Shield");
        
        // Build the Ship's Texture string in textures.r
        string shipType = m_PersistentShip->type;
        for(int i = 0; i < shipType.length(); i++)
        {
            if(shipType[i] == ' ')
            {
                shipType[i] = '-';
            }
        }
        
        stringstream shipTexture;
        if(strcmp( "default", m_PersistentShip->type.c_str() ) == 0)
        {
            shipTexture << "Ship-Default";
        }
        else
        {
            //shipTexture << "Ship-Default";
            //cout << "Ship-" << (m_PersistentShip->owner ? "Blue-" : "Red-") << m_PersistentShip->type << endl;
            shipTexture << "Ship-" << (m_PersistentShip->owner ? "Blue-" : "Red-") << shipType;
        }
        
        // Build the Explosion Texture
        stringstream shipExplosionTexture;
        shipExplosionTexture << "explosion-" << (int)(t * 89.0f);
        
        // Health Calculations
        const float upAngle = -90;
        const float healthSection = 100;
        m_PersistentShip->maxHealth = m_PersistentShip->maxHealth ? m_PersistentShip->maxHealth : 1;
        float healthLeft = m_PersistentShip->HealthOn(m_Turn, t) / m_PersistentShip->maxHealth;
        float healthStart = upAngle-healthSection*healthLeft;
        float healthEnd   = upAngle+healthSection*healthLeft;
        
        // Colors:
        Color teamColor[] = { Color(1, 0, 0, (shipIsExploding? 1 - t : shipStealth) ), Color(0, 0.4f, 1, (shipIsExploding? 1 - t : shipStealth) ) };
        float attackTrans = t * 2;
        if(t >= 0.5f)
        {
            attackTrans = 1 - (t - 0.5) * 2;
        }
        Color attackColor[] = { Color(1, 0, 0, attackTrans), Color(0, 0.4f, 1, attackTrans) };
        Color healthColor = Color(0, 1, 0, (shipIsExploding? 1 - t : shipStealth) );
        Color rangeColor = shipOwner ? Color(0, 0.4f, 1, attackTrans/4.0f + 0.25f) : Color(1, 0, 0, attackTrans/4.0f + 0.25f);
        // END: Variables we will need
        
        
        
        
        if(shipIsExploding)
        {
            game->renderer->setColor( Color(1, 1, 1) );
            game->renderer->drawTexturedQuad(shipCenter.x - shipRadius * 2.4f, shipCenter.y - shipRadius * 2.4f, shipRadius * 5.0f, shipRadius * 5.0f, shipExplosionTexture.str());
        }
        else
        {
            // Set the color to white for drawing the ship
            game->renderer->setColor( Color(1, 1, 1, shipStealth) );
            //game->renderer->drawTexturedQuad(shipCenter.x - shipRadius/1.25f, shipCenter.y - shipRadius/1.25f, shipRadius * 1.6f, shipRadius * 1.6f, shipTexture.str());
            drawRotatedTexturedQuad( game, shipCenter.x - shipRadius/1.25f, shipCenter.y - shipRadius/1.25f, shipRadius * 1.6f, shipHeading, shipTexture.str());
            if(renderShield)
            {
                drawRotatedTexturedQuad( game, shipCenter.x - shipRadius, shipCenter.y - shipRadius, shipRadius * 2, shipHeading, shipShieldTexture );
            }
        }
    
        // Draw their health
        if(renderShield)
        {
            game->renderer->setColor( teamColor[shipOwner] );
            game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthEnd, healthStart+360 );
            game->renderer->setColor( healthColor );
            game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthStart, healthEnd );
        }
        
        // Draw Attacks
        game->renderer->setColor( attackColor[shipOwner] );
        for(unsigned int i = 0; i < shipAttacks.size(); i++)
        {
            game->renderer->drawLine(shipCenter.x, shipCenter.y, shipAttacks[i].x, shipAttacks[i].y, 2); 
        }
        
        
        // Draw Range
        if(renderRange)
        {
            game->renderer->setColor( rangeColor );
            game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRange, 100 );
        }
        
    } // DrawPersistentShip::animation()
    
    
    
    void DrawPlayerHUD::animate( const float& t, AnimData * d, IGame* game )
    {
        
        game->renderer->setColor( m_PlayerHUD->id ? Color(0, 0.4f, 1, 1) : Color(1, 0, 0, 1) );
        // Draw the player's name
        game->renderer->drawText( m_PlayerHUD->NameX(), 20, "Roboto", m_PlayerHUD->name, 200 );
        
        // Draw the player's energy
        stringstream energy;
        energy << "Energy: " << m_PlayerHUD->energy;
        game->renderer->drawText( m_PlayerHUD->EnergyX(), 70, "Roboto", energy.str(), 100 );
        
        // Draw the player's victories
        stringstream victories;
        victories << "Victories: " << m_PlayerHUD->victories;
        game->renderer->drawText( m_PlayerHUD->VictoriesX(), 100, "Roboto", victories.str(), 100 );
        
        // Draw the player's time left
        game->renderer->drawText( m_PlayerHUD->TimeX(), 870, "Roboto", "Time Left:", 100 );
        stringstream time;
        time << m_PlayerHUD->time;
        game->renderer->drawText( m_PlayerHUD->TimeX(), 900, "Roboto", time.str(), 100 );
    }
    
    
    
    void DrawWarp::animate( const float& t, AnimData * d, IGame* game )
    {
      cout << "WARP" << endl;
        game->renderer->setColor( Color( 1, 1, 1 ) );
        float size = m_Warp->fadeOut ? 1 - t : t;
        drawRotatedTexturedQuad( game, m_Warp->x - size*m_Warp->radius, m_Warp->y - size*m_Warp->radius, size*m_Warp->radius * 2, t * 360.0f, "warp" );
    }

}
