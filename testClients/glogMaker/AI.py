#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"
    
  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))  
       
  def getRange(self, x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2   
        
  #Returns the x and y position of the nearest enemy
  def findNearest(self,ship,theirShips):
    distance = 10000; closestX = ship.getX(); closestY = ship.getY()
    for enemy in theirShips:
      if distance > self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY()):
        distance = self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY())        
        closestX = enemy.getX()
        closestY = enemy.getY()
    return [closestX,closestY]
      
  #Returns the the furthest point along a path to target      
  def moveTo(self,ship,x,y):
    distance = (((ship.getX() - x)**2) + ((ship.getY()- y)**2))**.5
    if ship.getType == "Warp Gate":
      distRatio = ship.getRange() / (1+distance)
    else:
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

              
  def spawnShips(self, player,friendlyWarpGate):
    energyLeft = self.players[player].getEnergy()
    while energyLeft > 5:
      selector = random.randrange(0,len(self.shipTypes)-1)
      if self.shipTypes[selector].getCost() < energyLeft:
        print self.shipTypes[selector].getType() + "warped in"
        self.shipTypes[selector].warpIn(friendlyWarpGate[0].getX(),friendlyWarpGate[0].getY())
        energyLeft -= self.shipTypes[selector].getCost()
        print energyLeft
        
              
  def init(self):      
    pass
    
  def end(self):
    pass    

  def run(self): 
    #if self.turnNumber() == 4 or self.turnNumber() == 5:
      #for ship in self.ships:
        #print str(ship.getType()) + "-" + str(ship.getOwner())
    #Variable declarations
    myShips = []
    theirShips = []
    FriendlyWarpGate = []
    EnemyWarpGate = []              

    #Find out who I am  
    player = 0    
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId()    
        
    #Creates a list of ships
    ships = self.ships  
    for ship in ships:
      if ship.getOwner() == player: 
        myShips.append(ship)
      else:
        theirShips.append(ship)
     
    #Locate my warp ship and their warp ship
    for ship in self.ships:
      if ship.getType() == "Warp Gate" and ship.getOwner() == player:
        FriendlyWarpGate.append(ship)
      elif ship.getType() == "Warp Gate" and ship.getOwner() != player:
        EnemyWarpGate.append(ship)            
    
    if (self.turnNumber() == 0 or self.turnNumber() == 1) and self.playerID() == player:
      self.spawnShips(player, FriendlyWarpGate)
      
    area = 1
    modifierX = random.randrange(-50,50) * (player+1)
    modifierY = random.randrange(-50,50) * (player+1)
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
            if furthestEnemy.getHealth() < ship.getDamage():
              ships.remove(furthestEnemy)
    
    return 1
    

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
      
  
      
