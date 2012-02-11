#ifndef CHESS_H
#define CHESS_H

#include <QObject>
#include "igame.h"
#include "animsequence.h"

// The Codegen's Parser
#include "parser/parser.h"
#include "parser/structures.h"

namespace visualizer
{
    class Space: public QObject, public AnimSequence, public IGame
    {
        Q_OBJECT;
        Q_INTERFACES( visualizer::IGame );
        public: 
            Space();
            ~Space();

            PluginInfo getPluginInfo();
            void loadGamelog( std::string gamelog );

            void load();
            void setup();

            void addCurrentBoard();
    
        private:
            parser::Game *m_game;  // The Game Object from parser/structures.h that is generated by the Codegen
  }; 

} // visualizer

#endif // CHESS_H
