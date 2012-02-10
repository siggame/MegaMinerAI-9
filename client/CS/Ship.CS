using System;
using System.Runtime.InteropServices;


///A space ship!
public class Ship
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;
  
  public Ship()
  {
  }
  
  public Ship(IntPtr p)
  {
    ptr = p;
    ID = Client.shipGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ships.Length; i++)
    {
      if(BaseAI.ships[i].ID == ID)
      {
        ptr = BaseAI.ships[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
    
    //commands
    
  ///
  public int move(int x, int y)
  {
    validify();
    return Client.shipMove(ptr, x, y);
  }
  ///
  public int selfDestruct()
  {
    validify();
    return Client.shipSelfDestruct(ptr);
  }
  ///
  public int attack(Ship target)
  {
    validify();
    target.validify();
    return Client.shipAttack(ptr, target.ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.shipGetId(ptr);
  }
  ///The owner of the piece
  public int getOwner()
  {
    validify();
    return Client.shipGetOwner(ptr);
  }
  ///Position x
  public int getX()
  {
    validify();
    return Client.shipGetX(ptr);
  }
  ///Position y
  public int getY()
  {
    validify();
    return Client.shipGetY(ptr);
  }
  ///ship size radius
  public int getRadius()
  {
    validify();
    return Client.shipGetRadius(ptr);
  }
  ///The ship type
  public string getType()
  {
    validify();
    return Client.shipGetType(ptr);
  }
  ///how many more attacks it has
  public int getAttacksLeft()
  {
    validify();
    return Client.shipGetAttacksLeft(ptr);
  }
  ///how much more movement it has
  public int getMovementLeft()
  {
    validify();
    return Client.shipGetMovementLeft(ptr);
  }
  ///the largest possible movement
  public int getMaxMovement()
  {
    validify();
    return Client.shipGetMaxMovement(ptr);
  }
  ///the max number of attacks it has
  public int getMaxAttacks()
  {
    validify();
    return Client.shipGetMaxAttacks(ptr);
  }
  ///the strength of its attacks
  public int getDamage()
  {
    validify();
    return Client.shipGetDamage(ptr);
  }
  ///the total health of the ship
  public int getHealth()
  {
    validify();
    return Client.shipGetHealth(ptr);
  }
  ///the max health possible for the ship
  public int getMaxHealth()
  {
    validify();
    return Client.shipGetMaxHealth(ptr);
  }

}
