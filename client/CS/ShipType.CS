using System;
using System.Runtime.InteropServices;


///An available ship type
public class ShipType
{
  public IntPtr ptr;
  protected int ID;
  protected int iteration;
  
  public ShipType()
  {
  }
  
  public ShipType(IntPtr p)
  {
    ptr = p;
    ID = Client.shipTypeGetId(ptr);
    iteration = BaseAI.iteration;
  }

  public bool validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.shipTypes.Length; i++)
    {
      if(BaseAI.shipTypes[i].ID == ID)
      {
        ptr = BaseAI.shipTypes[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
    
    //commands
    
  ///
  public int warpIn(int x, int y)
  {
    validify();
    return Client.shipTypeWarpIn(ptr, x, y);
  }
    
    //getters
    
  ///Unique Identifier
  public int getId()
  {
    validify();
    return Client.shipTypeGetId(ptr);
  }
  ///The ship type
  public string getType()
  {
    validify();
    return Client.shipTypeGetType(ptr);
  }
  ///The amount of money required to purchase this type of ship
  public int getCost()
  {
    validify();
    return Client.shipTypeGetCost(ptr);
  }

}
