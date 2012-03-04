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
    startX = int(ship.getX()*(1-distRatio))
    startY = int(ship.getY()*(1-distRatio))
    endX = int(x*distRatio)
    endY = int(y*distRatio)
    return [startX + endX, startY + endY]
   
  #Moves ship away from the nearest enemy
  def moveAway(self,ship,theirShips): 
    nearest = self.findNearest(ship,theirShips)
    points = self.moveTo(ship, nearest[0],nearest[1])
    newPoints = [ship.getX() + (ship.getX() - points[0]), ship.getY() + (ship.getY() - points[1])]
    ship.move(newPoints[0],newPoints[1])

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
              
  def spawnShips(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):
    #Spawning all ships on first turn
    energyLeft = self.players[player].getEnergy()
    #Spawn one high tier ship if available
    if availShips["Weapons Platform"] != 0:
      availShips["Weapons Platform"].warpIn(safeWarp[0],safeWarp[1])
      energyLeft -= availShips["Weapons Platform"].getCost()
    #Only spawn a Battleship if there are no Weapons Platforms
    elif availShips["Battleship"] != 0:
      availShips["Battleship"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Battleship"].getCost() 
    #Only spawn a Juggernaut if there are no Weapons Platforms or Battleships available 
    elif availShips["Juggernaut"] != 0:
      availShips["Juggernaut"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Juggernaut"].getCost()  
    #Only spawn a Cruiser as last resort 
    elif availShips["Cruiser"] != 0:
      availShips["Cruiser"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Cruiser"].getCost() 
      
    #Spawn 10 low tier ships if a high tier was purchased, 15 if not   
    if energyLeft < 50: 
      multiplier = 1
    else:
      multiplier = 1.5  
      
    if availShips["Bomber"] != 0:
      i = 10*multiplier
      while i > 0:
        availShips["Bomber"].warpIn(agressiveWarp[0],agressiveWarp[1])
        i-=1
        energyLeft -= availShips["Bomber"].getCost()
    #Only spawn interceptors if there are no bombers
    elif availShips["Interceptor"] != 0:
      i = 10*multiplier
      while i > 0:
        availShips["Interceptor"].warpIn(agressiveWarp[0],agressiveWarp[1])
        i-=1
        energyLeft -= availShips["Interceptor"].getCost()   
          
    #Spawning specialty ships (Initial design)        
    if availShips["Mine Layer"] != 0:
      while energyLeft > 5:
        availShips["Mine Layer"].warpIn(defensiveWarp[0],defensiveWarp[1])
        energyLeft -= availShips["Mine Layer"].getCost()                    
    if availShips["Support"] != 0 and energyLeft >= 5:
      availShips["Support"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Support"].getCost()
    elif availShips["EMP"] != 0 and energyLeft >= 5:
      while energyLeft > 0:
        availShips["EMP"].warpIn(agressiveWarp[0],agressiveWarp[1])
        energyLeft -= availShips["EMP"].getCost()   
    elif availShips["Stealth"] != 0 and energyLeft >= 5:
      while energyLeft > 0:
        availShips["Stealth"].warpIn(agressiveWarp[0],agressiveWarp[1])
        energyLeft -= availShips["Stealth"].getCost()   
        
  #Attack all enemies in range with all attacks
  def attackAllInRange(self,ship,theirShips):
    attackList = []
    attacksLeft = ship.getAttacksLeft()
    #Construct a list of all enemies in range
    for enemy in theirShips:
      #If in range and not a mine
      if self.getRange(ship.getX(),ship.getY(),ship.getRange(),enemy.getX(),enemy.getY(),enemy.getRadius()) and enemy.getType() != "Mine":
        attackList.append(enemy)
    #While I still have targets and attacks, attack!
    #TODO: Make ships prioritize special ships
    for target in attackList
      if attacksLeft > 0:
        ship.attack(target)
        #Remove them from possible targets if they died
        if target.getHealth() < ship.getDamage():
          theirShips.remove(target)  
        #Remove from list to prevent multi-hitting
        attacksLeft-=1
    attackList = []
    return attacksLeft
              
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
    availShips = {"Battleship" : 0,"Juggernaut" : 0,"Mine Layer" : 0,"Support" : 0, \
    "EMP" : 0,"Stealth" : 0,"Cruiser" : 0,"Weapons Platform" : 0,"Interceptor" : 0,"Bomber" : 0}
    #Establish library of all shipTypes available by name
    if self.turnNumber() == 0 or self.turnNumber() == 1:
      availShips = {"Battleship" : 0,"Juggernaut" : 0,"Mine Layer" : 0,"Support" : 0, \
      "EMP" : 0,"Stealth" : 0,"Cruiser" : 0,"Weapons Platform" : 0,"Interceptor" : 0,"Bomber" : 0}
      for shipType in self.shipTypes:
        availShips[shipType.getType()] = shipType            

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
     
   # print "Mine"
    #for ship in myShips:
    #  print ship.getType() + str(ship.getOwner())
    #print "Theirs"
    #for ship in theirShips:
    #  print ship.getType() + str(ship.getOwner())
      
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
    #Closest to enemy warpgate 
    agressiveWarp = self.moveTo(FriendlyWarpGate[0], EnemyWarpGate[0].getX(), EnemyWarpGate[0].getY())   
    #Closest to far edge
    safeWarp =  [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
    if abs(safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier) > 500:
      safeWarp = [499,0]
    else:
      safeWarp = [safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier, 0]
    #Center of my warp gate   
    defensiveWarp = [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
         
    #Spawn my ships on the first turn
    if (self.turnNumber() == 0 or self.turnNumber() == 1) and self.playerID() == player:
      self.spawnShips(player,availShips, safeWarp, defensiveWarp, agressiveWarp)
    
    #Ship move and attack:
      #Always self destruct if about to die
        #Try to optimize damage of explosion
      #General (Interceptor, Bomber, Cruiser, Juggernaut):
        #If can attack someone - hit and move max away
        #else move towards enemy closest to MY warp gate and try to attack after move
          #Dodge mines on the way
          #Advanced:
            #Spread out for EMP and Mine Layer
            #Priority to special ships in range
      #WP:
        #Stand in back and snipe special units -> lowest health -> WG
        #Move away from closest enemy
      #BC:
        #Head straight for enemy WG and fire along the way
      #Support:
        #Stay with the pack
      #Stealth 
        #Snipe special ships 
        #Weapons platform highest priority
      #EMP
        #Stay with group
        #Only fire at ships with > 50 health, enemy EMPs, or groups of 3 or more
      #Mine Layer
        #Surround the WG and WP with mines
        #Find a way to make multiple layers deep       
      
    for ship in myShips:
      if ship.getType() == "Interceptor" or ship.getType() == "Bomber" or ship.getType() == "Cruiser" or ship.getType() == "Juggernaut":
        #Try to attack everything in range    
        attacksLeft = self.attackAllInRange(ship,theirShips)
        #If all attacks expended, move away from enemies
        if attacksLeft == 0: 
          self.moveAway(ship,theirShips)        
        #Move towards enemies and try to attack again          
        else:
          points = self.findNearest(ship,theirShips)
          move = self.moveTo(ship,points[0],points[1])
          if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0:
            ship.move(move[0],move[1])
          attacksLeft = self.attackAllInRange(ship,theirShips)         
      elif ship.getType() == "Weapons Platform": 
        pass
      elif ship.getType() == "Battleship":
        pass
      elif ship.getType() == "Support":
        pass
      elif ship.getType() == "Stealth":
        pass
      elif ship.getType() == "EMP":
        pass
      elif ship.getType() == "Mine Layer":
        pass
      elif ship.getType() == "Warp Gate":
        pass
    
    return 1
    

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
      
  
      
