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
    return distance(x1, x2, y1, y2) <= rad1 + rad2
    
  def moveToNearest(self,ship):
    distance = 10000; closestX = 0; closestY = 0
    for enemy in ships:
      if ship.owner != player:
        if distance > self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY()):
          distance = self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY())        
        #if distance > (((ship.getX() - enemy.getX())**2) + ((ship.getY()- enemy.getY())**2))**.5:
          #distance = (((ship.getX() - enemy.getX())**2) + ((ship.getY()- enemy.getY())**2))**.5
          closestX = enemy.getX()
          closest = enemy.getY()
    self.moveTo(ship,closestX,closestY)
      
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
      return [startX + endX, startY + endY]

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

  def init(self):
        
    return 1

  def end(self):
    pass    

  def run(self): 
  
    #Variable declarations
    myShips = []
    theirShips = []
    FriendlyWarpGate = []
    EnemyWarpGate = []
    availShips = {"Battleship" : 0,"Juggernaut" : 0,"Mine Layer" : 0,"Support" : 0, \
      "EMP" : 0,"Stealth" : 0,"Cruiser" : 0,"Weapons Platform" : 0,"Interceptor" : 0,"Bomber" : 0}
      
    #Establish library of all shipTypes available by name
    if self.turnNumber() == 0 or self.turnNumber() == 1:
      for shipType in self.shipTypes:
        availShips[shipType] = shipType
          
    #Creates a list of ships
    ships = self.ships     

    #Find out who I am    
    player = 0    
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId()    

    #Locate my warp ship and their warp ship
    for ship in self.ships:
      if ship.getType() == "Warp Gate" and ship.getOwner() == player:
        FriendlyWarpGate.append(ship)
      elif ship.getType() == "Warp Gate" and ship.getOwner() != player:
        EnemyWarpGate.append(ship)            
 
    
    #Creates a modifier to help me move depending on which side of the map I spawned on
    modifier = -1
    if player == 1:
      modifier = 1
    #Setting general warp locations   
    #Closest to enemy ship
    agressiveWarp = self.moveTo(FriendlyWarpGate[0], EnemyWarpGate[0].getX(), EnemyWarpGate[0].getY())
    
    #Closest to far edge
    safeWarp =  [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
    if abs(safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier) > 500:
      safeWarp = [499,0]
    else:
      safeWarp = [safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier, 0]
      
    #Center of my warp gate
    defensiveWarp = [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
    
    
    if availShips["Weapons Platform"] != 0:
      warpSpot = [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
      availShips["Weapons Platform"].warpIn(warpSpot[0],warpSpot[1])
      
    
    #Start Old Code
    """
    modifierX = random.randrange(-50,50) * (player+1)
    modifierY = random.randrange(-50,50) * (player+1)
    for ship in ships:
      if ship.getType() != "Warp Gate" and ship.getType() != "Mine" and ship.getType() != "Weapons Platform" and ship.getOwner() == player:
        #Move weapons platform to the edge of the map
        if area < 75:
          if area%7 == 0:
            self.move(moveTo(ship,-250+modifierX,250-modifierY))
          elif area%7 == 1:
            self.move(ship,250+modifierX,-250-modifierY)
          elif area%7 == 2:
            self.move(ship,0+modifierX,0-modifierY)
          elif area%7 == 3:
            self.move(ship, 100+modifierX,100-modifierY)
          elif area%7 == 4:
            self.move(ship,-100+modifierX,-100-modifierY)
          elif area%7 == 5:
            self.move(ship,200+modifierX,-100-modifierY)
          elif area%7 == 6:
            self.move(ship,-100+modifierX,200-modifierY)
        else:
          self.moveToNearest(ship)
      area += 1 
    dist = 0
    """
    #End Old Code
    
    
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
