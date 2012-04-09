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

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    #Find each player's warp gate
    for ship in self.ships:
      #if this ship is of type Warp Gate
      if ship.getType() == "Warp Gate":
        #if you own this ship
        if ship.getOwner() == self.playerID:
          myGate = ship
        else:
          theirGate = ship
     
     #Warp in some ships
    for type in self.shipTypes:
      #If you have enough energy to warp in this type of ship
      if type.getCost() <= self.players[self.playerID].getEnergy():
        #Warp it in directly on top of your warp gate
        type.warpIn(myGate.getX(),myGate.getY())
    
    #Command your ships
    for ship in self.ships:
      x=y=0
      #If you own this ship, it can move, and it can attack
      if ship.getOwner() == self.playerID and ship.getMovementLeft()>0 and ship.getAttacksLeft()>0:
        #Find a point on the line connecting this ship and their warp gate is close enough for this ship to mve to.
        #x and y are our parameters    
        x,y = self.pointOnLine(ship.getX(),ship.getY(),theirGate.getX(),theirGate.getY(), ship.getMovementLeft())
        #If I have move to get there
        if ship.getX() != x or ship.getY()!= y:
          ship.move(x,y)
        if self.distance(ship.getX(),ship.getY(),theirGate.getX(),theirGate.getY())<= ship.getRange() + theirGate.getRadius():
          if theirGate.getHealth()>0:
            ship.attack(theirGate)
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
