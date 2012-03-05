#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "spaceAnimatable.h"
#include "irenderer.h"
#include "persistents.h"

namespace visualizer
{

    struct StartAnim: public Anim
    {
      public:
        void animate( const float& t, AnimData *d, IGame* game );

    };
    
  
    class DrawBackground: public Anim
    {
      public:
        void animate( const float& t, AnimData* d, IGame* game );

        float controlDuration() const
        { return 0; }

        float totalDuration() const
        { return 0; }

    }; // DrawBackground
  
    
    class DrawPersistentShip: public Anim
    {
        public:
            DrawPersistentShip( PersistentShip* persistentShip, int turn, int* mapRadius ) { m_PersistentShip = persistentShip; m_Turn = turn; m_MapRadius = mapRadius; }
            void animate( const float& t, AnimData *d, IGame* game );
            void drawRotatedTexturedQuad( IGame* game, float x, float y, float length, float degrees, string texture);
            
            float controlDuration() const
            { return 1; }
            float totalDuration() const
            { return 1; }
        private:
            PersistentShip* m_PersistentShip;
            int m_Turn;
            int* m_MapRadius;

    }; // DrawPersistentShip
    
    class DrawPlayerHUD: public Anim
    {
        public:
            DrawPlayerHUD( PlayerHUD* hud ) { m_PlayerHUD = hud; }
            void animate( const float& t, AnimData *d, IGame* game );

            float controlDuration() const
            { return 1; }
            float totalDuration() const
            { return 1; }
        private:
            PlayerHUD* m_PlayerHUD;
    }; // DrawPersistentShip

}

#endif // ANIMATION_H
