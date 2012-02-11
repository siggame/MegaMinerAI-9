#include "getters.h"

DLLEXPORT int playerGetId(_Player* ptr)
{
  return ptr->id;
}
DLLEXPORT char* playerGetPlayerName(_Player* ptr)
{
  return ptr->playerName;
}
DLLEXPORT float playerGetTime(_Player* ptr)
{
  return ptr->time;
}
DLLEXPORT int playerGetVictories(_Player* ptr)
{
  return ptr->victories;
}
DLLEXPORT int playerGetEnergy(_Player* ptr)
{
  return ptr->energy;
}
DLLEXPORT int shipGetId(_Ship* ptr)
{
  return ptr->id;
}
DLLEXPORT int shipGetOwner(_Ship* ptr)
{
  return ptr->owner;
}
DLLEXPORT int shipGetX(_Ship* ptr)
{
  return ptr->x;
}
DLLEXPORT int shipGetY(_Ship* ptr)
{
  return ptr->y;
}
DLLEXPORT int shipGetRadius(_Ship* ptr)
{
  return ptr->radius;
}
DLLEXPORT char* shipGetType(_Ship* ptr)
{
  return ptr->type;
}
DLLEXPORT int shipGetAttacksLeft(_Ship* ptr)
{
  return ptr->attacksLeft;
}
DLLEXPORT int shipGetMovementLeft(_Ship* ptr)
{
  return ptr->movementLeft;
}
DLLEXPORT int shipGetMaxMovement(_Ship* ptr)
{
  return ptr->maxMovement;
}
DLLEXPORT int shipGetMaxAttacks(_Ship* ptr)
{
  return ptr->maxAttacks;
}
DLLEXPORT int shipGetDamage(_Ship* ptr)
{
  return ptr->damage;
}
DLLEXPORT int shipGetRange(_Ship* ptr)
{
  return ptr->range;
}
DLLEXPORT int shipGetHealth(_Ship* ptr)
{
  return ptr->health;
}
DLLEXPORT int shipGetMaxHealth(_Ship* ptr)
{
  return ptr->maxHealth;
}
DLLEXPORT int shipTypeGetId(_ShipType* ptr)
{
  return ptr->id;
}
DLLEXPORT char* shipTypeGetType(_ShipType* ptr)
{
  return ptr->type;
}
DLLEXPORT int shipTypeGetCost(_ShipType* ptr)
{
  return ptr->cost;
}

