#include "animations.h"
#include "space.h"
#include "persistents.h"
#include <sstream>

namespace visualizer
{
  void drawRotatedTexturedQuad( IGame* game, float x, float y, float length, float degrees, string texture)
  {
    /*game->renderer->push();
      game->renderer->translate( 500, 500 );
      game->renderer->rotate( 45, 0, 0, 1 );
      game->renderer->drawQuad( -50, -50, 100, 100 );
      game->renderer->pop();*/

    //game->renderer->useShader( ((Space*)game)->programs["post"] );
    game->renderer->push();
    game->renderer->translate( x + length/2, y + length/2 );
    game->renderer->rotate( degrees, 0, 0, 1 );
    game->renderer->drawTexturedQuad( -1 * length/2, -1 * length/2, length, length, texture );
    game->renderer->pop();
    //game->renderer->useShader( 0 );
  }



  void StartAnim::animate( const float& /* t */, AnimData * /* d */, IGame* /*game*/ )
  {
  }


  void DrawBackground::animate( const float& /*t*/, AnimData * /*d*/, IGame* game )
  {
    stringstream ss;
    ss << "background-" << m_Background->random;
    game->renderer->setColor( Color( 1, 1, 1, 1 ) );
    game->renderer->drawTexturedQuad(0, 0, m_Background->radius * 2, m_Background->radius * 2, ss.str());
    //game->renderer->drawTexturedQuad(m_Background->outerRadius - m_Background->innerRadius, m_Background->outerRadius - m_Background->innerRadius, m_Background->innerRadius * 3, m_Background->innerRadius * 2, "planet");
    game->renderer->setColor( Color( 1, 1, 1, 0.1f ) );
    game->renderer->drawArc(500, 500, 500, 80 );
    
    if( game->options->getNumber( "Show Grid" ) )
    {
      game->renderer->drawLine( m_Background->radius, 0, m_Background->radius, m_Background->radius * 2, 1 );
      game->renderer->drawLine( 0, m_Background->radius, m_Background->radius * 2, m_Background->radius, 1 );
    }
  }

  void DrawRoundHUD::animate( const float& t, AnimData * /* d */, IGame* game )
  {
    stringstream round;
    round << "Round: " << (m_RoundHUD->round + 1) << "  Turn: " << m_RoundHUD->turn;
    game->renderer->setColor( Color( 1, 1, 1, 1 ) );
    game->renderer->drawText( m_RoundHUD->mapRadius, 1, "Roboto", round.str(), 100, IRenderer::Center);

    // Draw the t "hand"
    //game->renderer->drawArc( m_RoundHUD->mapRadius, m_RoundHUD->mapRadius, m_RoundHUD->mapRadius, 60, 0, 360.0f * t );
    
    // Draw the availible ship types
    if( game->options->getNumber( "Show Round's Ship Types" ) )
    {
      game->renderer->drawText( m_RoundHUD->mapRadius * 2.05, m_RoundHUD->mapRadius - 350, "Roboto", "Availible Ship Types:", 100 );
      int i = 0;
      for( auto& shiptype: m_RoundHUD->shipTypes )
      {
        game->renderer->drawText( m_RoundHUD->mapRadius * 2.1, m_RoundHUD->mapRadius - 300 + (i * 75), "Roboto", shiptype, 70 );
        
        stringstream shipTexture;
        shipTexture << "Ship-Red-";
        for(auto& character: shiptype)
        {
          if(character == ' ')
          {
            shipTexture << "-";
          }
          else
          {
            shipTexture << character;
          }
        }
        
        game->renderer->drawTexturedQuad( m_RoundHUD->mapRadius * 2.125, m_RoundHUD->mapRadius - 280 + (i * 75), 50, 50, shipTexture.str() );
        
        i++;
      }
    }

    // Draw the round end win screen
    if( m_RoundHUD->drawWinScreen && game->options->getNumber( "Display Round Winner" ) )
    {
      float op = t;
      stringstream winnerText;
      winnerText << "Winner: " << m_RoundHUD->winner;

      Color textColor = m_RoundHUD->winnerID == -1 ? Color( 0.1, 0.1, 0.1, op ) : ( m_RoundHUD->winnerID ? Color( 0, 0.4, 1, op ) : Color(1, 0, 0, op) );
      Color backgroundColor = Color( 1, 1, 1, op );

      game->renderer->setColor( backgroundColor );
      game->renderer->drawQuad( 0, 0, m_RoundHUD->mapRadius*2, m_RoundHUD->mapRadius*2 );

      game->renderer->setColor( textColor );
      game->renderer->drawText( m_RoundHUD->mapRadius, m_RoundHUD->mapRadius - 30, "Roboto", winnerText.str(), 300, IRenderer::Center );
      game->renderer->drawText( m_RoundHUD->mapRadius, m_RoundHUD->mapRadius + 70, "Roboto", m_RoundHUD->message, 170, IRenderer::Center );
    }
  }

  void DrawPersistentShip::animate( const float& t, AnimData * /*d*/, IGame* game )
  {
    // BEGIN: Variables we will need
    int shipOwner = m_PersistentShip->owner;
    glm::vec2 shipCenter = m_PersistentShip->LocationOn(m_Turn, t);
    shipCenter.x += *m_MapRadius;
    shipCenter.y += *m_MapRadius;
    // HeadingOn and LocationOn call the same function.  Should probably fix this
    // so it's less expensive.  2 per animate
    float shipHeading = m_PersistentShip->HeadingOn(m_Turn, t) * 57.3f + 270;
    float shipStealth = m_PersistentShip->StealthOn(m_Turn, t);
    bool shipIsEMPed = m_PersistentShip->EMPedOn(m_Turn);
    bool shipIsEMP = strcmp( "EMP", m_PersistentShip->type.c_str() ) == 0;
    bool shipIsSelected = m_PersistentShip->selected;
    vec2 idPosition = m_PersistentShip->m_idPositions[m_Turn];
    
    float shipSizeScale = game->options->getNumber( "Ship Render Size" ) / 100.0f;

    float shipRadius = m_PersistentShip->radius;
    bool shipIsExploding = m_PersistentShip->ExplodingOn(m_Turn);
    bool renderShield = m_PersistentShip->RenderShield();
    bool renderRange = m_PersistentShip->RenderRange();
    int shipRange = m_PersistentShip->range;

    vector<glm::vec2> shipAttacks = m_PersistentShip->AttacksOn( m_Turn, t );
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

    stringstream empedTexture;
    empedTexture << "emped-" << (m_PersistentShip->owner ? "red" : "blue"); // reversed because the enemy emps them, so it should be the ENEMY's color!

    stringstream empTexture;
    empTexture << "emp-" << (m_PersistentShip->owner ? "blue" : "red");

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
    
    // EMP Animation
    float animEmp[] = { 0.0f, 36.6f, 91.8f, 10.1f, 338.4f, 198.2f, 251.9f, 279.7f, 53.3f, 360.0f };
    float currentEmpAnim = animEmp[ int(t * 10.f) ];
    
    // Colors:
    Color teamColor = shipOwner ? Color(0, 0.4f, 1, (shipIsExploding? 1 - t : shipStealth)) : Color(1, 0, 0, (shipIsExploding? 1 - t : shipStealth));
    float attackTrans = t * 2;
    if(t >= 0.5f)
    {
      attackTrans = 1 - (t - 0.5) * 2;
    }
    
    Color teamBaseColor = shipOwner ? Color(0, 0.4f, 1, 1) : Color(1, 0, 0, 1);
    Color attackColor[] = { Color(1, 0, 0, attackTrans), Color(0, 0.4f, 1, attackTrans) };
    Color healthColor = Color(0, 1, 0, (shipIsExploding? 1 - t : shipStealth) );
    Color rangeColor = shipOwner ? Color(0, 0.4f, 1, attackTrans/4.0f + 0.25f) : Color(1, 0, 0, attackTrans/4.0f + 0.25f);
    Color normalColor = Color (1, 1, 1, 1);
    Color explosionColor = m_PersistentShip->SelfDestructs ? teamBaseColor : normalColor;
    // END: Variables we will need
    ////////////////////////////////////////////////////////////////////////////



    if( shipIsSelected )
    {
      game->renderer->setColor( Color(1, 1, 1) );
      game->renderer->drawTexturedQuad(shipCenter.x - shipRadius * 1.5, shipCenter.y - shipRadius * 1.5, shipRadius * 3.0f, shipRadius * 3.0f, "selected");
    }


    if(shipIsExploding)
    {
      game->renderer->setColor( explosionColor );
      game->renderer->drawTexturedQuad(shipCenter.x - shipRadius * 2.4f, shipCenter.y - shipRadius * 2.4f, shipRadius * 5.0f, shipRadius * 5.0f, shipExplosionTexture.str());
    }
    else
    {
      // Set the color to white for drawing the ship
      game->renderer->setColor( Color(1, 1, 1, shipStealth) );
      //game->renderer->drawTexturedQuad(shipCenter.x - shipRadius/1.25f, shipCenter.y - shipRadius/1.25f, shipRadius * 1.6f, shipRadius * 1.6f, shipTexture.str());
      drawRotatedTexturedQuad( game, shipCenter.x - shipRadius/1.25f * shipSizeScale, shipCenter.y - shipRadius/1.25f * shipSizeScale, shipRadius * 1.6f * shipSizeScale, shipHeading, shipTexture.str());
      
      if(renderShield && game->options->getNumber( "Display Ships' Sheild" ) )
      {
        drawRotatedTexturedQuad( game, shipCenter.x - shipRadius, shipCenter.y - shipRadius, shipRadius * 2, shipHeading, shipShieldTexture );
      }
    }

    // Draw their health
    if(renderShield)
    {
      game->renderer->setColor( teamColor );
      game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthEnd, healthStart+360 );
      game->renderer->setColor( healthColor );
      game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRadius, 100, healthStart, healthEnd );
    }



    if( shipIsEMPed )
    {
      game->renderer->setColor( normalColor );
      drawRotatedTexturedQuad( game, shipCenter.x - shipRadius, shipCenter.y - shipRadius, shipRadius * 2, shipHeading + currentEmpAnim, empedTexture.str() );
    }

    // Draw Attacks
    if(shipIsEMP && shipAttacks.size() > 0)
    {
      game->renderer->setColor( normalColor );
      drawRotatedTexturedQuad( game, shipCenter.x - shipRange, shipCenter.y - shipRange, shipRange * 2, shipHeading + currentEmpAnim, empTexture.str() );
    }
    else if (shipAttacks.size() > 0)
    {
      game->renderer->setColor( attackColor[shipOwner] );
      for(unsigned int i = 0; i < shipAttacks.size(); i++)
      {
        game->renderer->drawLine(shipCenter.x, shipCenter.y, shipAttacks[i].x, shipAttacks[i].y, 2); 
      }
    }

    // Draw Range
    if(renderRange || game->options->getNumber( "Display Ships' Range" ))
    {
      game->renderer->setColor( rangeColor );
      game->renderer->drawArc(shipCenter.x, shipCenter.y, shipRange, 100 );
    }

    if(m_Turn < m_PersistentShip->m_DeathTurn)
    {
      stringstream idName;
      idName << m_PersistentShip->id;

      game->renderer->setColor(Color(0, 0, 0));

      vec2 idp = vec2(idPosition.x + *m_MapRadius, idPosition.y + *m_MapRadius);
      idp -= vec2(15, 15);

      
      game->renderer->drawProgressBar(idp.x, idp.y + 2, 30, 15, 1, Color(1, 1, 1), 1, -10); 
      game->renderer->setColor(Color(1, 1, 1));

      game->renderer->translate(0, 0, -10);
      game->renderer->drawText(idp.x + 30/2, idp.y + 1, "Roboto", idName.str(), 58.0f, IRenderer::Alignment::Center);
      game->renderer->translate(0, 0, 10);

      game->renderer->drawLine(idp.x, idp.y, shipCenter.x, shipCenter.y, -9.0f);
    }
    

  } // DrawPersistentShip::animation()



  void DrawPlayerHUD::animate( const float&/* t */, AnimData * /* d*/, IGame* game )
  {
    IRenderer::Alignment align = m_PlayerHUD->id ? IRenderer::Left : IRenderer::Right;

    game->renderer->setColor( m_PlayerHUD->id ? Color(0, 0.4f, 1, 1) : Color(1, 0, 0, 1) );
    // Draw the player's name
    game->renderer->drawText( m_PlayerHUD->NameX(), 20, "Roboto", m_PlayerHUD->name, 200 , align);

    // Draw the player's energy
    stringstream energy;
    energy << "Energy: " << m_PlayerHUD->energy;
    game->renderer->drawText( m_PlayerHUD->EnergyX(), 70, "Roboto", energy.str(), 100, align );

    // Draw the player's victories
    stringstream victories;
    victories << "Victories: " << m_PlayerHUD->victories;
    game->renderer->drawText( m_PlayerHUD->VictoriesX(), 100, "Roboto", victories.str(), 100, align );

    // Draw the player's time left
    game->renderer->drawText( m_PlayerHUD->TimeX(), 870, "Roboto", "Time Left:", 100 );
    stringstream time;
    time << m_PlayerHUD->time;
    game->renderer->drawText( m_PlayerHUD->TimeX(), 900, "Roboto", time.str(), 100 );
  }



  void DrawWarp::animate( const float& t, AnimData * /*d*/, IGame* game )
  {
    game->renderer->setColor( Color( 1, 1, 1 ) );
    stringstream warpTexture;
    warpTexture << "warp-" << ( m_Warp->owner ? "blue" : "red" );
    float size = m_Warp->fadeOut ? 1 - t : t;
    drawRotatedTexturedQuad( game, m_Warp->x - size*m_Warp->radius, m_Warp->y - size*m_Warp->radius, size*m_Warp->radius * 2, t * 360.0f, warpTexture.str() );
  }

}
