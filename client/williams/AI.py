#-*-python-*-
from BaseAI import BaseAI
from GameObject import *

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  def init(self):
    pass

  def end(self):
    pass

  def run(self):
    #Find out who I am
    player = 0
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId() 
        
    #Locate my warp ship
    FriendlyWarpGate = []
    EnemyWarpGate = []
    for ship in self.ships:
      if ship.getType() == "Warp Gate" and ship.getOwner() == player:
        FriendlyWarpGate.append(ship)
      elif ship.getType() == "Warp Gate" and ship.getOwner() != player:
        EnemyWarpGate.append(ship)
    
    #Only perform these tests on the first turn
    if self.turnNumber() == 0 or self.turnNumber() == 1:  
      #Spawn one of each available ship
      #First attempt to spawn at invalid location 
      #Then spawn on outer edges of the Warp Gate      
      print "Try to spawn each type of ship at corners of Warp Gate range"
      area = 0
      for shipType in self.shipTypes:
        #Invalid spawn
        shipType.warpIn(1000,1000)
        #Top
        if area == 0:
          shipType.warpIn(FriendlyWarpGate[0].getX(),FriendlyWarpGate[0].getY()+FriendlyWarpGate[0].getRange())
        #Right
        if area == 0:
          shipType.warpIn(FriendlyWarpGate[0].getX()+FriendlyWarpGate[0].getRange(),FriendlyWarpGate[0].getY())
        #Bottom
        if area == 0:
          shipType.warpIn(FriendlyWarpGate[0].getX(),FriendlyWarpGate[0].getY()-FriendlyWarpGate[0].getRange())
        #Left
        if area == 0:
          shipType.warpIn(FriendlyWarpGate[0].getX()-FriendlyWarpGate[0].getRange(),FriendlyWarpGate[0].getY())
      
      print "Trying to move enemy ships and make them attack themselves"
      for ship in self.ships:
        if ship.getOwner() != player:
          ship.move(ship.getX()+5, ship.getY()+5)
          ship.attack(ship)
          
      print "Move all ships an invalid amount, then max range diagonally towards the enemy warp gate"
      distance = 0;distRatio = 0; startX = 0; startY = 0; endX = 0; endY = 0
      for ship in self.ships:
        if ship.getOwner() == player:
          distance = (((ship.getX() - EnemyWarpGate[0].getX())**2) + ((ship.getY() - EnemyWarpGate[0].getY())**2))**.5
          distRatio = ship.getMovementLeft() / distance
          startX = int(ship.getX()*distRatio)
          startY = int(ship.getY()*distRatio)
          endX = int(EnemyWarpGate[0].getX()*(1-distRatio))
          endY = int(EnemyWarpGate[0].getY()*(1-distRatio))
          print startX," ", endX," ",startY," ",endY
          ship.move(startX - endX - 1, startY - endY - 1)
          
      
    
        
  
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
