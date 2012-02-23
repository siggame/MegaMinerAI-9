using System;
using System.Runtime.InteropServices;

public class Client {
  [DllImport("client")]
  public static extern IntPtr createConnection();
  [DllImport("client")]
  public static extern int serverConnect(IntPtr connection, string host, string port);

  [DllImport("client")]
  public static extern int serverLogin(IntPtr connection, string username, string password);
  [DllImport("client")]
  public static extern int createGame(IntPtr connection);
  [DllImport("client")]
  public static extern int joinGame(IntPtr connection, int id, string playerType);

  [DllImport("client")]
  public static extern void endTurn(IntPtr connection);
  [DllImport("client")]
  public static extern void getStatus(IntPtr connection);

  [DllImport("client")]
  public static extern int networkLoop(IntPtr connection);


    //commands
  [DllImport("client")]
  public static extern int shipTypeWarpIn(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int playerTalk(IntPtr self, string message);
  [DllImport("client")]
  public static extern int shipMove(IntPtr self, int x, int y);
  [DllImport("client")]
  public static extern int shipSelfDestruct(IntPtr self);
  [DllImport("client")]
  public static extern int shipAttack(IntPtr self, IntPtr target);

    //accessors
  [DllImport("client")]
  public static extern int getTurnNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getPlayerID(IntPtr connection);
  [DllImport("client")]
  public static extern int getGameNumber(IntPtr connection);
  [DllImport("client")]
  public static extern int getRound(IntPtr connection);
  [DllImport("client")]
  public static extern int getVictoriesNeeded(IntPtr connection);
  [DllImport("client")]
  public static extern int getMapRadius(IntPtr connection);

  [DllImport("client")]
  public static extern IntPtr getShipType(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getShipTypeCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getPlayer(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getPlayerCount(IntPtr connection);
  [DllImport("client")]
  public static extern IntPtr getShip(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int getShipCount(IntPtr connection);


    //getters
  [DllImport("client")]
  public static extern int shipTypeGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern string shipTypeGetType(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipTypeGetCost(IntPtr ptr);

  [DllImport("client")]
  public static extern int playerGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern string playerGetPlayerName(IntPtr ptr);
  [DllImport("client")]
  public static extern float playerGetTime(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetVictories(IntPtr ptr);
  [DllImport("client")]
  public static extern int playerGetEnergy(IntPtr ptr);

  [DllImport("client")]
  public static extern int shipGetId(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetOwner(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetX(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetY(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetRadius(IntPtr ptr);
  [DllImport("client")]
  public static extern string shipGetType(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetAttacksLeft(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetMovementLeft(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetMaxMovement(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetMaxAttacks(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetDamage(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetRange(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetHealth(IntPtr ptr);
  [DllImport("client")]
  public static extern int shipGetMaxHealth(IntPtr ptr);


    //properties

}
