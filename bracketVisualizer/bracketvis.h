#ifndef BRACKETVIS_H
#define BRACKETVIS_H 

#include <QObject>
#include <QThread>
#include "igame.h"
#include "animsequence.h"

using namespace std;

namespace visualizer
{
    class BracketVis: public QThread, public AnimSequence, public IGame
    {
        Q_OBJECT;
        Q_INTERFACES( visualizer::IGame );
        public: 
            BracketVis();
            ~BracketVis();

            PluginInfo getPluginInfo();
            void loadGamelog( std::string gamelog );

            void destroy();

            void preDraw();
            void postDraw();

        private:
    }; 

} // visualizer

#endif // BRACKETVIS_H 
