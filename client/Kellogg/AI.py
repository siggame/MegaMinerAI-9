#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random

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
    ships = []
    enemy = []
    warpX = 0
    warpY = 0
    enemy_base = []
    warps = []
    player = 0
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId() 
    randShip = random.randrange(0,4)
    newshiptype = self.shipTypes[randShip]
    for ship in self.shipTypes:
       print "AAAA"
       if ship.getType() == "Warp Gate":
         warps.append(ship)
    for ship in self.ships:
       print "BBBB"
       print ship.getOwner(), " ", player
       if ship.getOwner() == player:
         print "-------"
         ships.append(ship)
       else:
         print "******"
         enemy.append(ship)
   
    for ship in ships:
      print "CCCC"
      if ship.getType() == "Warp Gate": 
         warpX = ship.getX()
         warpY = ship.getY() 
         newshiptype.warpIn(warpX,warpY)
      else:
       dirX = 0; dirY = 0
       if ship.getX() > 40:
          dirX = -1*ship.getMovementLeft()/4
          ship.move(ship.getX()+dirX,ship.getY())
       elif ship.getX() < 40:
          dirX = ship.getMovementLeft()/4
          ship.move(ship.getX()+dirX,ship.getY()) 
       else:
         if ship.getY() > 40:
           dirY = -1*ship.getMovementLeft()/4
           ship.move(ship.getX(),ship.getY()+dirY)
         elif ship.getY() <= 40:
           dirY = ship.getMovementLeft()/4
           ship.move(ship.getX(),ship.getY()+dirY) 
      
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
