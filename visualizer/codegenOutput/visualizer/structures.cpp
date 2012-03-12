// -*-c++-*-

#include "structures.h"

#include <iostream>

namespace parser
{


std::ostream& operator<<(std::ostream& stream, ShipType ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "type: " << ob.type  <<'\n';
  stream << "cost: " << ob.cost  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Player ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "playerName: " << ob.playerName  <<'\n';
  stream << "time: " << ob.time  <<'\n';
  stream << "victories: " << ob.victories  <<'\n';
  stream << "energy: " << ob.energy  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, Ship ob)
{
  stream << "id: " << ob.id  <<'\n';
  stream << "owner: " << ob.owner  <<'\n';
  stream << "x: " << ob.x  <<'\n';
  stream << "y: " << ob.y  <<'\n';
  stream << "radius: " << ob.radius  <<'\n';
  stream << "type: " << ob.type  <<'\n';
  stream << "attacksLeft: " << ob.attacksLeft  <<'\n';
  stream << "movementLeft: " << ob.movementLeft  <<'\n';
  stream << "maxMovement: " << ob.maxMovement  <<'\n';
  stream << "maxAttacks: " << ob.maxAttacks  <<'\n';
  stream << "damage: " << ob.damage  <<'\n';
  stream << "range: " << ob.range  <<'\n';
  stream << "health: " << ob.health  <<'\n';
  stream << "maxHealth: " << ob.maxHealth  <<'\n';
  stream << "selfDestructDamage: " << ob.selfDestructDamage  <<'\n';
  stream << "isStealthed: " << ob.isStealthed  <<'\n';
  stream << "isEMPd: " << ob.isEMPd  <<'\n';
  return stream;
}



std::ostream& operator<<(std::ostream& stream, move ob)
{
  stream << "move" << "\n";
  stream << "fromX: " << ob.fromX  <<'\n';
  stream << "fromY: " << ob.fromY  <<'\n';
  stream << "toX: " << ob.toX  <<'\n';
  stream << "toY: " << ob.toY  <<'\n';
  stream << "acting: " << ob.acting  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, selfDestruct ob)
{
  stream << "selfDestruct" << "\n";
  stream << "acting: " << ob.acting  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, attack ob)
{
  stream << "attack" << "\n";
  stream << "acting: " << ob.acting  <<'\n';
  stream << "target: " << ob.target  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, stealth ob)
{
  stream << "stealth" << "\n";
  stream << "acting: " << ob.acting  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, deStealth ob)
{
  stream << "deStealth" << "\n";
  stream << "acting: " << ob.acting  <<'\n';
  return stream;
}


std::ostream& operator<<(std::ostream& stream, GameState ob)
{
  stream << "turnNumber: " << ob.turnNumber  <<'\n';
  stream << "playerID: " << ob.playerID  <<'\n';
  stream << "gameNumber: " << ob.gameNumber  <<'\n';
  stream << "round: " << ob.round  <<'\n';
  stream << "victoriesNeeded: " << ob.victoriesNeeded  <<'\n';
  stream << "innerMapRadius: " << ob.innerMapRadius  <<'\n';
  stream << "outerMapRadius: " << ob.outerMapRadius  <<'\n';

  stream << "\n\nShipTypes:\n";
  for(std::map<int,ShipType>::iterator i = ob.shipTypes.begin(); i != ob.shipTypes.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nPlayers:\n";
  for(std::map<int,Player>::iterator i = ob.players.begin(); i != ob.players.end(); i++)
    stream << i->second << '\n';
  stream << "\n\nShips:\n";
  for(std::map<int,Ship>::iterator i = ob.ships.begin(); i != ob.ships.end(); i++)
    stream << i->second << '\n';
  stream << "\nAnimation\n";
  for
    (
    std::map< int, std::vector< SmartPointer< Animation > > >::iterator j = ob.animations.begin(); 
    j != ob.animations.end(); 
    j++ 
    )
  {
  for(std::vector< SmartPointer< Animation > >::iterator i = j->second.begin(); i != j->second.end(); i++)
  {
//    if((*(*i)).type == MOVE)
//      stream << *((move*)*i) << "\n";
//    if((*(*i)).type == SELFDESTRUCT)
//      stream << *((selfDestruct*)*i) << "\n";
//    if((*(*i)).type == ATTACK)
//      stream << *((attack*)*i) << "\n";
//    if((*(*i)).type == STEALTH)
//      stream << *((stealth*)*i) << "\n";
//    if((*(*i)).type == DESTEALTH)
//      stream << *((deStealth*)*i) << "\n";
  }
  

  }
  return stream;
}

Game::Game()
{
  winner = -1;
}

} // parser
