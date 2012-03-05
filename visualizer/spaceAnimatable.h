#ifndef CHESS_ANIMATABLE_H
#define CHESS_ANIMATABLE_H

#include "spaceAnimatable.h"
#include "irenderer.h"
#include "persistents.h"
#include "parser/structures.h"

#include "math.h"

namespace visualizer
{
    struct Background: public Animatable
    {
    };
    
    struct PersistentShipAnim: public Animatable
    {
    };
    
    class PlayerHUD: public Animatable
    {
        public:
            int id;
            string name;
            float time;
            int victories;
            int energy;
            bool winner;
        
        PlayerHUD( parser::Player player, bool win )
        {
            id = player.id;
            name = player.playerName;
            time = player.time;
            victories = player.victories;
            energy = player.energy;
            winner = win;
        }
        
        int NameX() { return (id ? 770 : 10); }
        int EnergyX() { return (id ? 810 : 10); }
        int TimeX() { return (id ? 850 : 40); }
        int VictoriesX() { return (id ? 840 : 10); }
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
