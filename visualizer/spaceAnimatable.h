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
        int innerRadius;
        int outerRadius;
        int turn;
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
    
    class RoundHUD: public Animatable
    {
        public:
            int turn;
            int round;
            string winner;
            int winnerID;
            int mapRadius;
            bool drawWinScreen;
            
            RoundHUD( int n, int t, string win, int id, int r, bool b )
            {
                round = n;
                turn = t;
                winner = win;
                winnerID = id;
                mapRadius = r;
                drawWinScreen = b;
            }
    };
    
    class Warp: public Animatable
    {
        public:
            int x;
            int y;
            int owner;
            int radius;
            bool fadeOut;
            
            Warp(int inX, int inY, int inRad, int inOwner, bool fade)
            {
                x = inX;
                y = inY;
                owner = inOwner;
                radius = inRad;
                fadeOut = fade;
            }
            
            Warp( Warp &warp )
            {
                x = warp.x;
                y = warp.y;
                owner = warp.owner;
                radius = warp.radius;
                fadeOut = warp.fadeOut;
            }
            
    };

} // visualizer

#endif // CHESS_ANIMATABLE_H
