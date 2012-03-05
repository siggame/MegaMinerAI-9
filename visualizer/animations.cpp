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
        game->renderer->setColor( Color( 1, 1, 1, 1 ) );
        game->renderer->drawTexturedQuad(0, 0, 2000, 2000, "background");
        game->renderer->setColor( Color( 1, 1, 1, 0.4f ) );
        game->renderer->drawLine(490, 500, 510, 500, 1);
        game->renderer->drawLine(500, 490, 500, 510, 1);
        game->renderer->drawArc(500, 500, 500, 50 );
    }
  
    
    void DrawPersistentShip::animate( const float& t, AnimData * d, IGame* game )
    {
        // BEGIN: Variables we will need
        SpacePoint shipCenter = m_PersistentShip->LocationOn(m_Turn, t);
        shipCenter.x += *m_MapRadius;
        shipCenter.y += *m_MapRadius;
        float shipStealth = m_PersistentShip->StealthOn(m_Turn, t);
        int shipOwner = m_PersistentShip->owner;
        float shipRadius = m_PersistentShip->radius;
        bool shipIsExploding = m_PersistentShip->ExplodingOn(m_Turn);
        
        vector< SpacePoint > shipAttacks = m_PersistentShip->AttacksOn( m_Turn );
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
        Color attackColor[] = { Color(1, 0, 0, t), Color(0, 0, 1, t) };
        Color healthColor = Color(0, 1, 0, (shipIsExploding? 1 - t : shipStealth) );
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
            game->renderer->drawTexturedQuad(shipCenter.x - shipRadius/1.25f, shipCenter.y - shipRadius/1.25f, shipRadius * 1.6f, shipRadius * 1.6f, shipTexture.str());
            game->renderer->drawTexturedQuad(shipCenter.x - shipRadius, shipCenter.y - shipRadius, shipRadius * 2.38f, shipRadius * 2.38f, shipShieldTexture);
        }
    
        // Draw their health
        game->renderer->setColor( teamColor[shipOwner] );
        game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthEnd, healthStart+360 );
        game->renderer->setColor( healthColor );
        game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthStart, healthEnd );
        
        // Draw Attacks
        game->renderer->setColor( attackColor[shipOwner] );
        for(unsigned int i = 0; i < shipAttacks.size(); i++)
        {
            game->renderer->drawLine(shipCenter.x, shipCenter.y, shipAttacks[i].x, shipAttacks[i].y, 2); 
        }
        
    } // DrawPersistentShip::animation()
    
    
    void DrawPlayerHUD::animate( const float& t, AnimData * d, IGame* game )
    {
        game->renderer->setColor( m_PlayerHUD->id ? Color(1, 0, 0, 1) : Color(0, 0.4f, 1, 1) );
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

}
