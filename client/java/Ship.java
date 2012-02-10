import com.sun.jna.Pointer;

///A space ship!
class Ship
{
  Pointer ptr;
  int ID;
  int iteration;
  public Ship(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.shipGetId(ptr);
    iteration = BaseAI.iteration;
  }
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.ships.length; i++)
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
  int move(int x, int y)
  {
    validify();
    return Client.INSTANCE.shipMove(ptr, x, y);
  }
  ///
  int selfDestruct()
  {
    validify();
    return Client.INSTANCE.shipSelfDestruct(ptr);
  }
  ///
  int attack(Ship target)
  {
    validify();
    target.validify();
    return Client.INSTANCE.shipAttack(ptr, target.ptr);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.INSTANCE.shipGetId(ptr);
  }
  ///The owner of the piece
  public int getOwner()
  {
    validify();
    return Client.INSTANCE.shipGetOwner(ptr);
  }
  ///Position x
  public int getX()
  {
    validify();
    return Client.INSTANCE.shipGetX(ptr);
  }
  ///Position y
  public int getY()
  {
    validify();
    return Client.INSTANCE.shipGetY(ptr);
  }
  ///ship size radius
  public int getRadius()
  {
    validify();
    return Client.INSTANCE.shipGetRadius(ptr);
  }
  ///The ship type
  public String getType()
  {
    validify();
    return Client.INSTANCE.shipGetType(ptr);
  }
  ///how many more attacks it has
  public int getAttacksLeft()
  {
    validify();
    return Client.INSTANCE.shipGetAttacksLeft(ptr);
  }
  ///how much more movement it has
  public int getMovementLeft()
  {
    validify();
    return Client.INSTANCE.shipGetMovementLeft(ptr);
  }
  ///the largest possible movement
  public int getMaxMovement()
  {
    validify();
    return Client.INSTANCE.shipGetMaxMovement(ptr);
  }
  ///the max number of attacks it has
  public int getMaxAttacks()
  {
    validify();
    return Client.INSTANCE.shipGetMaxAttacks(ptr);
  }
  ///the strength of its attacks
  public int getDamage()
  {
    validify();
    return Client.INSTANCE.shipGetDamage(ptr);
  }
  ///the total health of the ship
  public int getHealth()
  {
    validify();
    return Client.INSTANCE.shipGetHealth(ptr);
  }
  ///the max health possible for the ship
  public int getMaxHealth()
  {
    validify();
    return Client.INSTANCE.shipGetMaxHealth(ptr);
  }

}
