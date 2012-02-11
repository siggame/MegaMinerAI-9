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
  
    class DrawBoard: public Anim
    {
      public:
        void animate( const float& t, AnimData* d, IGame* game );

        float controlDuration() const
        { return 0; }

        float totalDuration() const
        { return 0; }

    }; // DrawBoard
  
    class DrawSpacePiece: public Anim
    {
      public:
        DrawSpacePiece( SpacePiece* piece ) { m_piece = piece; }

        void animate( const float& t, AnimData* d, IGame* game );
      private:
        SpacePiece* m_piece;
        
    }; // DrawSpacePiece

}

#endif // ANIMATION_H
