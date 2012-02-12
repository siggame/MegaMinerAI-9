#ifndef ANIMATIONS_H
#define ANIMATIONS_H

#include "spaceAnimatable.h"
#include "irenderer.h"

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
        
    }; // DrawSpacePiece

}

#endif // ANIMATION_H
