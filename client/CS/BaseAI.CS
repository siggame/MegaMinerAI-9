using System;
using System.Runtime.InteropServices;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
  public static Player[] players;
  public static Ship[] ships;
  public static ShipType[] shipTypes;
  IntPtr connection;
  public static int iteration;
  bool initialized;

  public BaseAI(IntPtr c)
  {
    connection = c;
  }
    
  ///
  ///Make this your username, which should be provided.
  public abstract String username();
  ///
  ///Make this your password, which should be provided.
  public abstract String password();
  ///
  ///This is run on turn 1 before run
  public abstract void init();
  ///
  ///This is run every turn . Return true to end the turn, return false
  ///to request a status update from the server and then immediately rerun this function with the
  ///latest game status.
  public abstract bool run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public bool startTurn()
  {
    iteration++;
    int count = 0;
    count = Client.getPlayerCount(connection);
    players = new Player[count];
    for(int i = 0; i < count; i++)
    {
      players[i] = new Player(Client.getPlayer(connection, i));
    }
    count = Client.getShipCount(connection);
    ships = new Ship[count];
    for(int i = 0; i < count; i++)
    {
      ships[i] = new Ship(Client.getShip(connection, i));
    }
    count = Client.getShipTypeCount(connection);
    shipTypes = new ShipType[count];
    for(int i = 0; i < count; i++)
    {
      shipTypes[i] = new ShipType(Client.getShipType(connection, i));
    }

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


  ///How many turns it has been since the beginning of the game
  public int turnNumber()
  {
    return Client.getTurnNumber(connection);
  }
  ///Player Number; either 0 or 1
  public int playerID()
  {
    return Client.getPlayerID(connection);
  }
  ///What number game this is for the server
  public int gameNumber()
  {
    return Client.getGameNumber(connection);
  }
  ///What round you are in the match
  public int round()
  {
    return Client.getRound(connection);
  }
  ///How many victories a player needs to win
  public int victoriesNeeded()
  {
    return Client.getVictoriesNeeded(connection);
  }
  ///The radius of the map.  Center of screen is (0,0), with +x right, +y up
  public int mapRadius()
  {
    return Client.getMapRadius(connection);
  }
}
