#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

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

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
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
       if ship.getType() == "Warp Gate":
         warps.append(ship)
    for ship in self.ships:
       if ship.getOwner() == player:
         ships.append(ship)
         print len(ships)
       else:
         enemy.append(ship)
         print len(enemy)
    for ship in ships:
      if ship.getType() == "Warp Gate": 
         warpX = ship.getX()
         warpY = ship.getY() 
         newshiptype.warpIn(warpX,warpY)
      else:
       for foe in enemy:
         if self.inRange(ship.getX(),ship.getY(), ship.getRadius(), foe.getX(), foe.getY(), foe.getRadius()):
           print "AAA"
           while ship.getAttacksLeft()>0:
            print "BBB"
            ship.attack(foe)    
       dirX = 0; dirY = 0
       move_list = [1,1,1,1,1]
       for i in move_list:
         if ship.getX() > 30:
            dirX = -1*ship.getMovementLeft()/4
            ship.move(ship.getX()+dirX,ship.getY())
         elif ship.getX() < 30:
            dirX = ship.getMovementLeft()/4
            ship.move(ship.getX()+dirX,ship.getY()) 
         elif ship.getX() == 30:
           if ship.getY() > 30:
             print "c"
             dirY = -1*ship.getMovementLeft()/4
             ship.move(ship.getX(),ship.getY()+dirY)
           elif ship.getY() < 30:
             print "d"
             dirY = ship.getMovementLeft()/4
             ship.move(ship.getX(),ship.getY()+dirY) 
           else:
             ship.move(ship.getX(),ship.getY()+1)
         else:
           ship.move(ship.getX()+1,ship.getY()) 
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
