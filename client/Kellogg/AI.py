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
       
    randShip = random.randrange(0,4)
    newshiptype = self.shipTypes[randShip]
    for ship in self.shipTypes:
       if ship.getType() == "Warp Gate":
         warps.append(ship)
    for ship in self.ships 
       enemy.append(ship)
     for e in enemy:
       if e.getType() == "Warp Gate":
         enemy_base.append(e)
      
    newshiptype.warpIn(warpX,warpY)
    for ship in ships:
      print ship.getType()
    for ship in ships:
       print ship.getType(), ship.getX(),ship.getY()
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
       print ship.getX()+dirX, ship.getY()+dirY
      
    #ship.move((ship.getX()+ship.getMovementLeft()/5)*-1,(ship.getY()+ship.getMovementLeft()/5)*-1)
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
