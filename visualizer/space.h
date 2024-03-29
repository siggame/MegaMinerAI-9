#ifndef CHESS_H
#define CHESS_H

#include <QObject>
#include <QThread>
#include "igame.h"
#include "animsequence.h"
#include <map>
#include <string>
#include "persistents.h"

// The Codegen's Parser
#include "parser/parser.h"
#include "parser/structures.h"

using namespace std;

namespace visualizer
{
    class Space: public QThread, public AnimSequence, public IGame
    {
        Q_OBJECT;
        Q_INTERFACES( visualizer::IGame );
        public: 
            Space();
            ~Space();

            PluginInfo getPluginInfo();
            void loadGamelog( std::string gamelog );

            void run();
            void setup();
            void destroy();

            void preDraw();
            void postDraw();

            void addCurrentBoard();
    
            map<string, int> programs;
            
            list<int> getSelectedUnits();
        private:
            parser::Game *m_game;  // The Game Object from parser/structures.h that is generated by the Codegen
            int m_mapRadius;
            bool m_suicide;
            map< int, PersistentShip* > m_PersistentShips; // The PersistentShips from which ship animations are made
    }; 

} // visualizer

#endif // CHESS_H
