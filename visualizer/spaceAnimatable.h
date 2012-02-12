#ifndef CHESS_ANIMATABLE_H
#define CHESS_ANIMATABLE_H

#include "spaceAnimatable.h"
#include "irenderer.h"

namespace visualizer
{
    struct Background: public Animatable
    {
    };
  
    struct SpacePiece: public Animatable
    {
        int x;
        int y;
        int owner;
        int type;
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
