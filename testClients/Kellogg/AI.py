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
    warp = []
    battleship = []
    juggernaut = []
    miner = []
    support = []
    emp = []
    stealth = []
    crusier = []
    weapons = []
    interceptor = []
    bomber = []
    avail = []
    for ship in self.shipTypes:
      if ship.getType() == "Stealth":
        print "WARNING: STEALTH SHIPS ARE AVAILABLE"
      avail.append(ship.getType())
    print avail  

  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  def run(self):
    print len(warp)
    for type in self.shipTypes:
      print type.getType()
    myships = []
    enemy = []
    randShip = random.randrange(0,4)
    newshiptype = self.shipTypes[randShip]
 
    #distinguish my ships from enemy ships
    for ship in self.ships:
       if ship.getOwner() == self.playerID():
         myships.append(ship)
       elif ship.getOwner() != self.playerID():
         enemy.append(ship)
    
    for ship in myships:
       move = ship.getMaxMovement()
       attack = ship.getMaxAttacks()
       #warp in ships
       if ship.getType() == "Warp Gate": 
         newshiptype.warpIn(ship.getX(),ship.getY())
       #attacky stuff
       for foe in enemy:
          if ship.getAttacksLeft()>0:
           if ship.getType() == "Mine Layer" and self.distance(ship.getX(),ship.getY(),foe.getX(),foe.getY())<=ship.getRange():
             ship.attack(ship)                   
           elif self.inRange(ship.getX(),ship.getY(), ship.getRadius(), foe.getX(), foe.getY(), foe.getRadius()):
             ship.attack(foe)
       #movey stuff
       dirX = 0; dirY = 0; randX = 0; randY = 0
       randX = random.randrange(-10,10)
       randY = random.randrange(-10,10)
       while move > 0:
         if ship.getX() > 0:
            dirX = -1*ship.getMovementLeft()/5
         elif ship.getX() < 0:
            dirX = ship.getMovementLeft()/5
         if ship.getY() > 10:
           dirY = -1*ship.getMovementLeft()/5
         elif ship.getY() < 10:
           dirY = ship.getMovementLeft()/5
         dis = self.distance(ship.getX(),ship.getY(),ship.getX()+dirX,ship.getY()+dirY)
         if dis <= ship.getMovementLeft() and  dis >0:
           ship.move(ship.getX()+dirX,ship.getY()+dirY)
         move -= dis
       if self.turnNumber()%100 >= 95:
         ship.selfDestruct()
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
