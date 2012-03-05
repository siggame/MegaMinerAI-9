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
  
    class DrawSpaceShip: public Anim
    {
      public:
        DrawSpaceShip( SpaceShip* spaceShip ) { m_spaceShip = spaceShip; }

        void animate( const float& t, AnimData* d, IGame* game );
      private:
        SpaceShip* m_spaceShip;
        
    }; // DrawSpaceShip
    
    class DrawShipAttack: public Anim
    {
        public:
            DrawShipAttack( AttackData* attack ) { m_attackData = attack; }
            void animate( const float& t, AnimData *d, IGame* game );

            float controlDuration() const
            { return 1; }
            float totalDuration() const
            { return 1; }
        private:
            AttackData* m_attackData;

    }; // ShipAttack
    
    
    
    class DrawPersistentShip: public Anim
    {
        public:
            DrawPersistentShip( PersistentShip* persistentShip, int turn, int* mapRadius ) { m_PersistentShip = persistentShip; m_Turn = turn; m_MapRadius = mapRadius; }
            void animate( const float& t, AnimData *d, IGame* game );

            float controlDuration() const
            { return 1; }
            float totalDuration() const
            { return 1; }
        private:
            PersistentShip* m_PersistentShip;
            int m_Turn;
            int* m_MapRadius;

    }; // DrawPersistentShip

}

#endif // ANIMATION_H
