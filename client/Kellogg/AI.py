#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Kellogg"

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
       else:
         enemy.append(ship)
    for ship in ships:
      if ship.getType() == "Warp Gate": 
         newshiptype.warpIn(ship.getX(),ship.getY())
      else:
       attack_list = [1,1,1,1]
       for foe in enemy:
         if self.inRange(ship.getX(),ship.getY(), ship.getRadius(), foe.getX(), foe.getY(), foe.getRadius()):
           for i in attack_list:
            print ship.getAttacksLeft(), "ATTACKS LEFT"
            ship.attack(foe)
         elif ship.getType() == "Mine Layer":
           ship.attack(ship)
       dirX = 0; dirY = 0
       move_list = [1,1,1,1,1,1,1,1,1,1,1,1]
       for i in move_list:
         if ship.getMovementLeft() >= int(2*ship.getMovementLeft()/3):
            ship.move(ship.getX()+random.randrange(-10,10),ship.getY()+random.randrange(-10,10))
         if ship.getX() > 0:
            dirX = -1*ship.getMovementLeft()/5
         elif ship.getX() < 0:
            dirX = ship.getMovementLeft()/5
         if ship.getX() <= 20 or ship.getX() >= -20:
           if ship.getY() > 10:
             dirY = -1*ship.getMovementLeft()/5
           elif ship.getY() < 10:
             dirY = ship.getMovementLeft()/5
           else:
             ship.move(ship.getX(),ship.getY()+1)
         ship.move(ship.getX()+dirX,ship.getY()+dirY) 
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
