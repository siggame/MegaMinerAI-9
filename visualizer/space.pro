INCLUDEPATH +=  ../interfaces \
                ../common/ \
                ./parser/

DEPENDPATH += ../common/ 

TEMPLATE = lib
TARGET = space
SOURCES = *.cpp \
          ./parser/*.cpp \
          ./parser/sexp/*.cpp

HEADERS +=  *.h \
            ./parser/*.h \
            ./parser/sexp/*.h

CONFIG += debug plugin dll
debug:DEFINES += __DEBUG__
#QMAKE_CFLAGS_DEBUG += -pg
#QMAKE_CXXFLAGS_DEBUG += -pg
QMAKE_LFLAGS_DEBUG += -shared -Wl
QMAKE_LFLAGS_RELEASE += -shared -Wl
DEFINES += YY_NO_UNISTD_H PERFT_FAST
DESTDIR = ../plugins/

QT += opengl
