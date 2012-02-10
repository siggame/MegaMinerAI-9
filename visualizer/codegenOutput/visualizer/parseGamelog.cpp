#include "parser.h"
#include "sexp/sexp.h"
#include "sexp/parser.h"
#include "sexp/sfcompat.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>

#include <iostream>

using namespace std;

namespace parser
{

char *ToLower( char *str )
{
  for( int i = 0; i < strlen( str ); i++ )
  {
    str[ i ] = tolower( str[ i ] );
  }
  return str;
}


static bool parsePlayer(Player& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.playerName = new char[strlen(sub->val)+1];
  strncpy(object.playerName, sub->val, strlen(sub->val));
  object.playerName[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.time = atof(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.victories = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parsePlayer.\n Parsing: " << *expression << endl;
    return false;
  }

  object.energy = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseShip(Ship& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.owner = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.x = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.y = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.radius = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.type = new char[strlen(sub->val)+1];
  strncpy(object.type, sub->val, strlen(sub->val));
  object.type[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.attacksLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.movementLeft = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxMovement = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxAttacks = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.damage = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.health = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShip.\n Parsing: " << *expression << endl;
    return false;
  }

  object.maxHealth = atoi(sub->val);
  sub = sub->next;

  return true;

}
static bool parseShipType(ShipType& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  sub = expression->list;

  if ( !sub ) 
  {
    cerr << "Error in parseShipType.\n Parsing: " << *expression << endl;
    return false;
  }

  object.id = atoi(sub->val);
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShipType.\n Parsing: " << *expression << endl;
    return false;
  }

  object.type = new char[strlen(sub->val)+1];
  strncpy(object.type, sub->val, strlen(sub->val));
  object.type[strlen(sub->val)] = 0;
  sub = sub->next;

  if ( !sub ) 
  {
    cerr << "Error in parseShipType.\n Parsing: " << *expression << endl;
    return false;
  }

  object.cost = atoi(sub->val);
  sub = sub->next;

  return true;

}

static bool parseAttack(attack& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = ATTACK;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.acting = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parseattack.\n Parsing: " << *expression << endl;
    return false;
  }
  object.target = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseDeStealth(deStealth& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = DESTEALTH;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsedeStealth.\n Parsing: " << *expression << endl;
    return false;
  }
  object.acting = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseMove(move& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = MOVE;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.fromY = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toX = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.toY = atoi(sub->val);
  sub = sub->next;
  if( !sub ) 
  {
    cerr << "Error in parsemove.\n Parsing: " << *expression << endl;
    return false;
  }
  object.acting = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseSelfDestruct(selfDestruct& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = SELFDESTRUCT;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parseselfDestruct.\n Parsing: " << *expression << endl;
    return false;
  }
  object.acting = atoi(sub->val);
  sub = sub->next;
  return true;

}
static bool parseStealth(stealth& object, sexp_t* expression)
{
  sexp_t* sub;
  if ( !expression ) return false;
  object.type = STEALTH;
  sub = expression->list->next;
  if( !sub ) 
  {
    cerr << "Error in parsestealth.\n Parsing: " << *expression << endl;
    return false;
  }
  object.acting = atoi(sub->val);
  sub = sub->next;
  return true;

}

static bool parseSexp(Game& game, sexp_t* expression)
{
  sexp_t* sub, *subsub;
  if( !expression ) return false;
  expression = expression->list;
  if( !expression ) return false;
  if(expression->val != NULL && strcmp(expression->val, "status") == 0)
  {
    GameState gs;
    while(expression->next != NULL)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(sub->val) == "game")
      {
          sub = sub->next;
          if ( !sub ) return false;
          gs.turnNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.playerID = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.gameNumber = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.round = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.victoriesNeeded = atoi(sub->val);
          sub = sub->next;
          if ( !sub ) return false;
          gs.mapRadius = atoi(sub->val);
          sub = sub->next;
      }
      else if(string(sub->val) == "Player")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Player object;
          flag = parsePlayer(object, sub);
          gs.players[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "Ship")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          Ship object;
          flag = parseShip(object, sub);
          gs.ships[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
      else if(string(sub->val) == "ShipType")
      {
        sub = sub->next;
        bool flag = true;
        while(sub && flag)
        {
          ShipType object;
          flag = parseShipType(object, sub);
          gs.shipTypes[object.id] = object;
          sub = sub->next;
        }
        if ( !flag ) return false;
      }
    }
    game.states.push_back(gs);
  }
  else if(string(expression->val) == "animations")
  {
    std::map< int, std::vector< SmartPointer< Animation > > > animations;
    while(expression->next)
    {
      expression = expression->next;
      sub = expression->list;
      if ( !sub ) return false;
      if(string(ToLower( sub->val ) ) == "attack")
      {
        SmartPointer<attack> animation = new attack;
        if ( !parseAttack(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "de-stealth")
      {
        SmartPointer<deStealth> animation = new deStealth;
        if ( !parseDeStealth(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "move")
      {
        SmartPointer<move> animation = new move;
        if ( !parseMove(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "self-destruct")
      {
        SmartPointer<selfDestruct> animation = new selfDestruct;
        if ( !parseSelfDestruct(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
      if(string(ToLower( sub->val ) ) == "stealth")
      {
        SmartPointer<stealth> animation = new stealth;
        if ( !parseStealth(*animation, expression) )
          return false;

        animations[ ((AnimOwner*)&*animation)->owner ].push_back( animation );
      }
    }
    game.states[game.states.size()-1].animations = animations;
  }
  else if(string(expression->val) == "ident")
  {
    expression = expression->next;
    if ( !expression ) return false;
    sub = expression->list;
    while(sub)
    {
      subsub = sub->list;
      if ( !subsub ) return false;
      int number = atoi(subsub->val);
      if(number >= 0)
      {
        subsub = subsub->next;
        if ( !subsub ) return false;
        subsub = subsub->next;
        if ( !subsub ) return false;
        game.players[number] = subsub->val;
      }
      sub = sub->next;
    }
  }
  else if(string(expression->val) == "game-winner")
  {
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    expression = expression->next;
    if ( !expression ) return false;
    game.winner = atoi(expression->val);
		expression = expression->next;
		if( !expression ) return false;
		game.winReason = expression->val;
  }

  return true;
}


bool parseFile(Game& game, const char* filename)
{
  //bool value;
  FILE* in = fopen(filename, "r");
  //int size;
  if(!in)
    return false;

  parseFile(in);

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      fclose(in);
      return false;
    }
    destroy_sexp(st);
  }

  fclose(in);

  return true;
}


bool parseGameFromString(Game& game, const char* string)
{

  parseString( string );

  sexp_t* st = NULL;

  while((st = parse()))
  {
    if( !parseSexp(game, st) )
    {
      while(parse()); //empty the file, keep Lex happy.
      return false;
    }
    destroy_sexp(st);
  }

  return true;
}

} // parser
