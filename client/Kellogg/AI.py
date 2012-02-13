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

  def distance(fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(x1, y1, rad1, x2, y2, rad2):
    return distance(x1, x2, y1, y2) <= rad1 + rad2
      
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
         warpX = ship.getX()
         warpY = ship.getY() 
         newshiptype.warpIn(warpX,warpY)
      else:
       for foe in enemy:
#         if self.inRange(x1, y1, rad1, x2, y2, rad2):
           ship.attack(foe)    
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
