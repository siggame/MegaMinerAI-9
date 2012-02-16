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
    for ship in self.shipTypes:
      if ship.getType() == "Stealth":
        print "WARNING: STEALTH SHIPS ARE AVAILABLE"

  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  def run(self):
    myships = set()
    enemy = set()
    player = 0
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId() 
    comme = """randShip = random.randrange(0,4)
    newshiptype = self.shipTypes[randShip]
    for ship in self.ships:
       if ship.getOwner() == player:
         myships.add(ship)
       elif ship.getOwner() != player:
         enemy.add(ship)"""
    for ship in self.ships:
      if ship.getOwner() == player:
  #     if ship.getType() == "Warp Gate": 
 #      newshiptype.warpIn(ship.getX(),ship.getY())
       comment = """attack_list = [1,1,1]
       for foe in enemy:
        if ship.getAttacksLeft()>0:
         if self.inRange(ship.getX(),ship.getY(), ship.getRadius(), foe.getX(), foe.getY(), foe.getRadius()):
           for i in attack_list:
            ship.attack(foe)
         elif ship.getType() == "Mine Layer" and self.distance(ship.getX(),ship.getY(),foe.getX(),foe.getY())<=ship.getRange():
           ship.attack(ship)
       dirX = 0; dirY = 0; randX = 0; randY = 0
       move_list = [1,1,1,1]
       randX = random.randrange(-10,10)
       randY = random.randrange(-10,10)
       print "HEY"""
       i = 0
       if 1 == 1 :#while ship.getMovementLeft() > 0:
         print "while loop print ",ship.getMovementLeft()
         comment = """ if ship.getX() > 0:
            dirX = -1*ship.getMovementLeft()/5
         elif ship.getX() < 0:
            dirX = ship.getMovementLeft()/5
         #if ship.getX() <= 20 or ship.getX() >= -20:
         if ship.getY() > 10:
           dirY = -1*ship.getMovementLeft()/5
         elif ship.getY() < 10:
           dirY = ship.getMovementLeft()/5
         print dirX,dirY
         dis = self.distance(ship.getX(),ship.getY(),ship.getX()+dirX,ship.getY()+dirY)
         print "dis", dis
         if dis <= ship.getMovementLeft() and  dis >0:
           print "dirX ",dirX, "dirY ", dirY
           print "distance ",self.distance(ship.getX(),ship.getY(),ship.getX()+dirX,ship.getY()+dirY) 
           print ship.getMovementLeft()
           #call move here
           ship.move(ship.getX()+dirX,ship.getY()+dirY+)
           print ship.getMovementLeft()
        
         print "gah"""
         ship.move(ship.getX()+ship.getMaxMovement(),ship.getY())
         print "after move",ship.getMovementLeft(), "max move", ship.getMaxMovement()
         i+=1
         print "i = ",i
       #if self.turnNumber()%100 >= 95:
       #  ship.selfDestruct()
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
