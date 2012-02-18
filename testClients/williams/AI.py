#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random
myShips = []
theirShips = []


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
       
  def getRange(self, x1, y1, rad1, x2, y2, rad2):
    return distance(x1, x2, y1, y2) <= rad1 + rad2
    
  def moveToNearest(self,ship):
    distance = 9000; closestX = 0; closestY = 0
    for enemy in ships:
      if ship.owner != player:
        if distance > (((ship.getX() - enemy.getX())**2) + ((ship.getY()- enemy.getY())**2))**.5:
          distance = (((ship.getX() - enemy.getX())**2) + ((ship.getY()- enemy.getY())**2))**.5
          closestX = enemy.getX()
          closest = enemy.getY()
    self.moveTo(ship,closestX,closestY)
      
    
  def moveTo(self,ship,x,y):
    distance = (((ship.getX() - x)**2) + ((ship.getY()- y)**2))**.5
    distRatio = ship.getMovementLeft() / (1+distance)
    if distance < 15:
      pass
    elif distRatio > 1:
      ship.move(x,y)
    else:
      distRatio /= 2
      startX = int(ship.getX()*(1-distRatio))
      startY = int(ship.getY()*(1-distRatio))
      endX = int(x*distRatio)
      endY = int(y*distRatio)
      ship.move(startX + endX, startY + endY)

  def attackFurthestUnit(self,ship,target):
    for enemy in self.ships:
      if ship.getAttacksLeft() >= 1 and ship.getOwner() != enemy.getOwner():
        if self.getRange(ship.getX(),ship.getY(),ship.getRange(),enemy.getX(),enemy.getY(),enemy.getRadius()):
          if ship.getType() == "Mine Layer":
            ship.attack(ship)
            pass
          else:
            if ship.getType() != "Mine":
              ship.attack(enemy)       

  def run(self):
    #Find out who I am
    
    player = 0
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId() 
        
    ships = self.ships
    
    #Locate my warp ship
    FriendlyWarpGate = []
    EnemyWarpGate = []
    for ship in ships:
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
      
          
     
    distance = 0;distRatio = 0; startX = 0; startY = 0; endX = 0; endY = 0
    area = 1
    modifierX = random.randrange(-50,50) * (player+1)
    modifierY = random.randrange(-50,50) * (player+1)
    
    #Moving my ships
    for ship in ships:
      if ship.getType() != "Warp Gate" and ship.getType() != "Mine" and ship.getType() != "Weapons Platform" and ship.getOwner() == player:
        #Move weapons platform to the edge of the map
        if area < 75:
          if area%7 == 0:
            self.moveTo(ship,-250+modifierX,250-modifierY)
          elif area%7 == 1:
            self.moveTo(ship,250+modifierX,-250-modifierY)
          elif area%7 == 2:
            self.moveTo(ship,0+modifierX,0-modifierY)
          elif area%7 == 3:
            self.moveTo(ship, 100+modifierX,100-modifierY)
          elif area%7 == 4:
            self.moveTo(ship,-100+modifierX,-100-modifierY)
          elif area%7 == 5:
            self.moveTo(ship,200+modifierX,-100-modifierY)
          elif area%7 == 6:
            self.moveTo(ship,-100+modifierX,200-modifierY)
        else:
          self.moveToNearest(ship)
      area += 1 
    dist = 0
    for ship in ships:
      furthestDist = -1
      furthestEnemy = ships[0]
      if ship.getOwner() == player:
        if ship.getAttacksLeft() > 0:
          for enemy in ships:
            if enemy.getOwner() != player: 
              dist = self.distance(ship.getX(),enemy.getX(),ship.getY(),enemy.getY())
              if dist < ship.getRange() + enemy.getRadius() and dist > furthestDist:
                furthestEnemy = enemy
                furthestDist = dist
          if furthestDist != -1:
            ship.attack(furthestEnemy)
            
     
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
