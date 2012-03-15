#ifndef GETTERS_H 
#define GETTERS_H
#include "vc_structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

namespace client
{

#ifdef __cplusplus
extern "C" {
#endif

DLLEXPORT int shipTypeGetId(_ShipType* ptr);
DLLEXPORT char* shipTypeGetType(_ShipType* ptr);
DLLEXPORT int shipTypeGetCost(_ShipType* ptr);


DLLEXPORT int playerGetId(_Player* ptr);
DLLEXPORT char* playerGetPlayerName(_Player* ptr);
DLLEXPORT float playerGetTime(_Player* ptr);
DLLEXPORT int playerGetVictories(_Player* ptr);
DLLEXPORT int playerGetEnergy(_Player* ptr);


DLLEXPORT int shipGetId(_Ship* ptr);
DLLEXPORT int shipGetOwner(_Ship* ptr);
DLLEXPORT int shipGetX(_Ship* ptr);
DLLEXPORT int shipGetY(_Ship* ptr);
DLLEXPORT int shipGetRadius(_Ship* ptr);
DLLEXPORT char* shipGetType(_Ship* ptr);
DLLEXPORT int shipGetAttacksLeft(_Ship* ptr);
DLLEXPORT int shipGetMovementLeft(_Ship* ptr);
DLLEXPORT int shipGetMaxMovement(_Ship* ptr);
DLLEXPORT int shipGetMaxAttacks(_Ship* ptr);
DLLEXPORT int shipGetDamage(_Ship* ptr);
DLLEXPORT int shipGetRange(_Ship* ptr);
DLLEXPORT int shipGetHealth(_Ship* ptr);
DLLEXPORT int shipGetMaxHealth(_Ship* ptr);
DLLEXPORT int shipGetSelfDestructDamage(_Ship* ptr);



#ifdef __cplusplus
}
#endif

}

#endif
