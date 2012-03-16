#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

myShips = []
theirShips = []
shipHealth = {}
locs = []
myMines = []
detonate = True
priorityList = {"Battleship" : 6.5,"Juggernaut" : 4,"Mine Layer" : 8.5,"Support" : 8, "Warp Gate" : 0, \
    "EMP" : 7,"Stealth" : 10,"Cruiser" : 3,"Weapons Platform" : 9,"Interceptor" : 1,"Bomber" : 2, "Mine" : -2}

#FEATURE LIST:
  #Move to support ships
  #Optimize code       
    
class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Waffle"

  @staticmethod
  def password():
    return "password"
    
  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))  
       
  def getRange(self, x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2 

  def pointsAtEdge(self,X,Y,r,n): 
    pi = 3.14159265  
    points = [(int(math.floor((X + math.cos(2*pi/n*x)*r))),int(math.floor((Y + math.sin(2*pi/n*x)*r)))) for x in xrange(0,n+1)] 
    return points     
        
  #Returns the x and y position of the nearest enemy
  def findNearest(self,ship):
    distance = 10000; closestX = ship.getX(); closestY = ship.getY()
    for enemy in theirShips:
      if distance > self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY()) and enemy.getType() != "Mine":
        distance = self.distance(ship.getX(), enemy.getX(), ship.getY(),enemy.getY())        
        closestX = enemy.getX()
        closestY = enemy.getY()
    return [closestX,closestY]
       
  def moveToInjured(self, ship):
    weakestShip = myShips[0]
    for myShip in myShips:
      if (myShip.getHealth()/myShip.getMaxHealth())  <= (weakestShip.getHealth() / weakestShip.getMaxHealth()) and myShip.getId() != ship.getId() \
      and myShip.getType() != "Mine":
        weakestShip = myShip
    move = self.moveTo(ship, weakestShip.getX(), weakestShip.getY(), locs, detonate)
    if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
      ship.move(move[0], move[1])    
      
  #Returns the the furthest point along a path to target      
  def moveTo(self,ship,x,y,locs,detonate):
    #Gets point furthest along a path between ship and target location
    distance = (((ship.getX() - x)**2) + ((ship.getY() - y)**2))**.5
    distRatio = 0
    if distance == 0:
      return [x,y]
    if ship.getType() == "Warp Gate":
      distRatio = ship.getRange() / distance
    else:
      distRatio = ship.getMovementLeft() / (distance*1.10)
    startX = int(ship.getX()*(1-distRatio))
    startY = int(ship.getY()*(1-distRatio))
    endX = int(x*distRatio)
    endY = int(y*distRatio)
    finalX = startX + endX
    finalY = startY + endY
    #Checks to see if there is a mine or a friendly ship at shortest location and that the ship is within bounds of the map
    goodMove = True
    for enemy in theirShips:
      if enemy.getType() == "Mine":
        if self.getRange(finalX, finalY, ship.getRadius(), enemy.getX(), enemy.getY(), enemy.getRange()):  
          goodMove = False
    for friend in myShips:
      if self.getRange(finalX, finalY, ship.getRadius(), friend.getX(), friend.getY(), friend.getRadius()/2):  
        goodMove = False
    if self.distance(0, finalX, 0, finalY) + ship.getRadius() > self.outerMapRadius() \
    or self.distance(0, finalX, 0, finalY) - ship.getRadius() < self.innerMapRadius():
      goodMove = False
    if ship.getType() == "Mine Layer":
      for mine in myMines:
        if self.getRange(finalX, finalY, 30, mine[0], mine[1], 30):
          goodMove = False 
    #If any of the above conditions are false, generate points in a circle around the ship
    if goodMove == False:
      points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,32)
      points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,24))
      distance = 10000
      #Iterate through all of these points to find which is the "best"
      for point in points:
        #Check to see if ship is within bounds of map
        if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.outerMapRadius() \
        and self.distance(0, point[0], 0, point[1]) - ship.getRadius() > self.innerMapRadius():
          goodMove = True
          #Check for mines
          for enemy in theirShips:
            if enemy.getType() == "Mine":
              if self.getRange(point[0], point[1], ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
                goodMove = False
          #Check for friendly ships. Locs contains a list of all of the moves that have occured.
          for loc in locs:
            if self.getRange(point[0], point[1], ship.getRadius()/2, loc[0], loc[1], 0):  
              goodMove = False
          #If a mine layer, make sure no mines are nearby
          if ship.getType() == "Mine Layer":
            for mine in myMines:
              if self.getRange(point[0], point[1], 30, mine[0], mine[1], 30):
                goodMove = False 
          #If all criteria met, check to see if this point is closer to target                
          if goodMove == True:
            if self.distance(point[0], x ,point[1], y) < distance:
              distance = self.distance(point[0], x , point[1], y)
              finalX = point[0]
              finalY = point[1]
    #Check to see if my best move is on a mine. If so, set detonate to false so no other ships will blow up.
     # if detonate == True:
        #for enemy in theirShips:
          #if enemy.getType() == "Mine":
            #if self.getRange(finalX, finalY, ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
              #detonate = False
    return [finalX, finalY]
   
  #Moves ship away from the nearest enemy
  def moveAway(self,ship): 
    finalX = finalY = 0
    nearest = self.findNearest(ship)
    points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,32)
    points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,24))
    distance = 0
    for point in points:
      if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.outerMapRadius() \
      and self.distance(0, point[0], 0, point[1]) - ship.getRadius() > self.innerMapRadius():
        goodMove = True
        for enemy in theirShips:
          if enemy.getType() == "Mine":
            if self.getRange(point[0], point[1], ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
              goodMove = False
        for loc in locs:
          if self.getRange(point[0], point[1], ship.getRadius()/2, loc[0], loc[1], 0):  
            goodMove = False
        if goodMove == True:
          if self.distance(point[0],nearest[0],point[1],nearest[1]) > distance:
            distance = self.distance(point[0],nearest[0],point[1],nearest[1])
            finalX = point[0]
            finalY = point[1]
    if self.distance(ship.getX(),finalX, ship.getY(),finalY) > 0:
      ship.move(finalX,finalY)
              
  #Spawn small ships until you reach input energy value
  def spawnSmall(self, energyStart, energyLeft, availShips, safeWarp, defensiveWarp, agressiveWarp):
    if availShips["Bomber"] != 0 or availShips["Interceptor"] != 0:
      while energyStart > energyLeft:
        if availShips["Bomber"] != 0:
          availShips["Bomber"].warpIn(agressiveWarp[0],agressiveWarp[1])
          energyStart -= availShips["Bomber"].getCost()
        if availShips["Interceptor"] != 0 and availShips["Battleship"] == 0:
          availShips["Interceptor"].warpIn(agressiveWarp[0],agressiveWarp[1])
          energyStart -= availShips["Interceptor"].getCost()
    return energyStart

  def spawnBig(self, energyLeft, availShips, safeWarp, defensiveWarp, agressiveWarp):   
    if availShips["Mine Layer"] != 0 and availShips["Weapons Platform"] != 0 and energyLeft >= availShips["Weapons Platform"].getCost():
      availShips["Weapons Platform"].warpIn(safeWarp[0],safeWarp[1])
      energyLeft -= availShips["Weapons Platform"].getCost()
    elif availShips["Battleship"] != 0 and availShips["Mine Layer"] == 0 and energyLeft >= availShips["Battleship"].getCost():
      availShips["Battleship"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Battleship"].getCost() 
    elif (availShips["Interceptor"] != 0 or availShips["Bomber"] != 0) and availShips["Juggernaut"] != 0 and energyLeft >= availShips["Juggernaut"].getCost():
      availShips["Juggernaut"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Juggernaut"].getCost() 
    elif availShips["Cruiser"] != 0 and energyLeft >= availShips["Cruiser"].getCost():
      availShips["Cruiser"].warpIn(agressiveWarp[0],agressiveWarp[1])
      energyLeft -= availShips["Cruiser"].getCost()  
    elif availShips["Weapons Platform"] != 0 and energyLeft >= availShips["Weapons Platform"].getCost():
      availShips["Weapons Platform"].warpIn(safeWarp[0],safeWarp[1])
      energyLeft -= availShips["Weapons Platform"].getCost()
    return energyLeft

  def spawnSpecial(self, energyLeft, availShips, safeWarp, defensiveWarp, agressiveWarp):
    if energyLeft > 5:  
      if availShips["Mine Layer"] != 0:
        availShips["Mine Layer"].warpIn(defensiveWarp[0],defensiveWarp[1])
        energyLeft -= availShips["Mine Layer"].getCost() 
      if availShips["Support"] != 0 and energyLeft > 5:
        availShips["Support"].warpIn(agressiveWarp[0],agressiveWarp[1])
        energyLeft -= availShips["Support"].getCost()
      elif availShips["EMP"] != 0:
        availShips["EMP"].warpIn(agressiveWarp[0],agressiveWarp[1])
        energyLeft -= availShips["EMP"].getCost() 
      elif availShips["Stealth"] != 0:
        availShips["Stealth"].warpIn(agressiveWarp[0],agressiveWarp[1])
        energyLeft -= availShips["Stealth"].getCost()  
    return energyLeft

  def fillerSpawn(self, energyLeft, availShips, cheapest, safeWarp, defensiveWarp, agressiveWarp):    
    while energyLeft > cheapest:
      for type in availShips:
        if availShips[type] != 0 and availShips[type].getCost() <= energyLeft:
          availShips[type].warpIn(agressiveWarp[0],agressiveWarp[1])
          energyLeft -= availShips[type].getCost()      
    return energyLeft          
   
  def spawnShips(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):
    energyLeft = self.players[player].getEnergy() 
    cheapest = 100
    for type in availShips:
      if availShips[type] != 0 and availShips[type].getCost() < cheapest:
        cheapest =  availShips[type].getCost()
    energyLeft = self.spawnSmall(energyLeft, 20, availShips, safeWarp, defensiveWarp, agressiveWarp)
    energyLeft = self.spawnSpecial(energyLeft, availShips, safeWarp, defensiveWarp, agressiveWarp)
    energyLeft = self.spawnBig(energyLeft, availShips, safeWarp, defensiveWarp, agressiveWarp)
    energyLeft = self.fillerSpawn(energyLeft, availShips, cheapest, safeWarp, defensiveWarp, agressiveWarp)
        
  #Finds the highest priority enemy based on the defined list above
  #Will either be passed in all of their ships or a set of units in range
  def highestPriorityEnemy(self,attackList):
    if len(attackList) > 0:
      target = attackList[0]      
      for enemy in attackList:
        if enemy.getType() != "Mine":      
          if priorityList[target.getType()] < priorityList[enemy.getType()]:
            target = enemy  
      return target
    else:
      return myShips[0]      
    
  #Attack all enemies in range with all attacks
  def attackAllInRange(self, ship, attacks, attackedList):
    #Create a list of things I've attacked and things I can attack
    #AttackedList will be used if multiple attack phases occur in one turn
    attackedList = attackedList
    attackList = []
    attacksLeft = attacks
    #If EMP or Mine Layer only attack once per turn
    if ship.getType() == "EMP" or ship.getType() == "Mine Layer":
      attacksLeft = 1
    #Construct a list of all enemies in range
    for enemy in theirShips:
      #If in range and not a mine
      if self.getRange(ship.getX(),ship.getY(),ship.getRange(),enemy.getX(),enemy.getY(),enemy.getRadius()) and enemy.getType() != "Mine" \
      and enemy not in attackedList:
        attackList.append(enemy) 
    stacked = len(attackedList)        
    if (ship.getType() == "EMP" or ship.getType() == "Mine Layer") and len(attackList) > 2:
      ship.attack(ship)
    else:
      #While I still have targets and attacks, attack!
      #TODO: Handle support damage and health modifiers
      while attacksLeft > 0 and len(attackList) > 0:
        target = self.highestPriorityEnemy(attackList)
        #If I have attacks, they have health left, and they are not mine => Attack them
        if attacksLeft > 0 and shipHealth[target.getId()] > 0 and target.getOwner() != ship.getOwner():
          shipHealth[target.getId()] -= ship.getDamage()
          #If I killed them, remove them from list of possible targets
          if shipHealth[target.getId()] <= ship.getDamage() and target.getId() in theirShips:
            theirShips.remove(target)
          else:
            attackedList.append(target)
          ship.attack(target)
          attacksLeft-=1
          attackList.remove(target)
          print ship.getId(), ship.getAttacksLeft(), attacksLeft
        else:
          attackList.remove(target)
      del attackList[0:len(attackList)]  
    #If more than 5 enemies are stacked up, self destruct on them for massive damage! Awww yeah!      
    if stacked > 5:
      self.blowUp(ship)     
    return [attacksLeft, attackedList]
    
  #Smart self-destruct. Moves to nearest enemy and then explodes
  def blowUp(self,ship):
    points = self.findNearest(ship)
    move = self.moveTo(ship, points[0], points[1], [], detonate)
    if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
      ship.move(move[0],move[1])
    if self.getRange(move[0],move[1],ship.getRadius(), points[0], points[1], 30):
      ship.selfDestruct()
      for enemy in theirShips:
        if self.getRange(move[0],move[1],ship.getRadius(), enemy.getX(), enemy.getY(), enemy.getRadius()):
          shipHealth[enemy.getId()] -= ship.getSelfDestructDamage()
          if (enemy.getHealth() - ship.getSelfDestructDamage()) <= 0:
            theirShips.remove(enemy)
              
  def init(self):      
    pass
    
  def end(self):
    pass    

  def run(self): 
    detonate = True
    #Reset all of my globals
    del locs[0:len(locs)]
    del myShips[0:len(myShips)]
    del theirShips[0:len(theirShips)]
    FriendlyWarpGate = []
    EnemyWarpGate = []   
    
    #Establish library of all shipTypes available by name
    availShips = {"Battleship" : 0,"Juggernaut" : 0,"Mine Layer" : 0,"Support" : 0, \
    "EMP" : 0,"Stealth" : 0,"Cruiser" : 0,"Weapons Platform" : 0,"Interceptor" : 0,"Bomber" : 0}
    for shipType in self.shipTypes:
      availShips[shipType.getType()] = shipType      

    #Find out who I am
    player = 0    
    for i in self.players:
      if i.getId() == self.playerID():
        player = i.getId()    
        
    #Creates a list my ships and enemy ships
    ships = self.ships  
    for ship in ships:
      if ship.getOwner() == player: 
        myShips.append(ship)
      else:
        theirShips.append(ship)
        shipHealth[ship.getId()] = ship.getHealth()
           
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
    agressiveWarp = self.moveTo(FriendlyWarpGate[0], EnemyWarpGate[0].getX(), EnemyWarpGate[0].getY(),locs, detonate)   
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
      self.spawnShips(player, availShips, safeWarp, defensiveWarp, agressiveWarp)
      
    defensiveLayer = False
      
    for ship in myShips:
      #If a ship is below 25% health, find the nearest enemy and self destruct
      if ship.getHealth() <= (ship.getMaxHealth()*.25) and ship.getType() != "Warp Gate":
        self.attackAllInRange(ship, ship.getAttacksLeft(), []) 
        self.blowUp(ship)
      #General ship type. Move to highest priority target and attack
      elif ship.getType() == "Interceptor" or ship.getType() == "Bomber" or ship.getType() == "Cruiser" or \
      ship.getType() == "Juggernaut" or ship.getType() == "EMP" or ship.getType() == "Battleship" \
      or (ship.getType() == "Mine Layer" and defensiveLayer == True):
        #Try to attack everything in range    
        attackData = self.attackAllInRange(ship, ship.getAttacksLeft(),[])
        #If all attacks expended, move away from enemies
        if attackData[0] == 0: 
          if ship.getType() != "EMP":
            self.moveAway(ship) 
          else:
            self.blowUp(ship)          
        #Move towards enemies and try to attack again          
        else:
          target = self.highestPriorityEnemy(theirShips)
          move = self.moveTo(ship,target.getX(),target.getY(),locs, detonate)
          if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
            locs.append(move)
            ship.move(move[0],move[1])
          attacksLeft = self.attackAllInRange(ship, attackData[0], attackData[1]) 
      #If I have mine layers, hide behind the field and fire, else move away from nearest enemy and attack          
      elif ship.getType() == "Weapons Platform": 
        if availShips["Mine Layer"] != 0:       
          if player == 0:
            move = self.moveTo(ship,((self.outerMapRadius()-1)*-1), 0,locs, detonate)          
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) < ship.getMovementLeft():
              ship.move(move[0], move[1])
              locs.append(move)
          else:
            move = self.moveTo(ship,self.outerMapRadius()-1, 0,locs, detonate) 
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) < ship.getMovementLeft():
              ship.move(move[0],move[1])
              locs.append(move)
        else:
          self.moveAway(ship)    
        self.attackAllInRange(ship, ship.getAttacksLeft(), []) 
      #Move to the weakest ally 
      elif ship.getType() == "Support":
        self.moveToInjured(ship)        
      elif ship.getType() == "Stealth":
        target = self.highestPriorityEnemy(theirShips)
        hasAttacked = False
        #Only attack if I can run away afterwards
        if self.getRange(ship.getX(), ship.getY(), ship.getRange(), target.getX(), target.getY(), target.getRadius()):
          shipHealth[target.getId()] -= ship.getDamage()
          if shipHealth[target.getId()] <= ship.getDamage() and target.getId() in theirShips:
            theirShips.remove(target)
          ship.attack(target)
          self.moveAway(ship)
        else:
          move = self.moveTo(ship,target.getX(),target.getY(),locs, detonate)
          if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
            ship.move(move[0],move[1])
            locs.append(move)
      #Defensive mine layers will place a mine field around the warp gate. Offensive will drop mines on enemies
      elif ship.getType() == "Mine Layer":
        defensiveLayer = True 
        if ship.getAttacksLeft() > 0:
          move = self.moveTo(ship,FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY(),locs, detonate)
          if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
            ship.move(move[0],move[1])
            locs.append(move)
          if self.turnNumber() >=4:                
            ship.attack(ship) 
            myMines.append([ship.getX(), ship.getY()])                      
        else:
          self.blowUp(ship)
      #If I have mine layers, hide behind them. Otherwise move away from nearest enemy
      elif ship.getType() == "Warp Gate":  
        if availShips["Mine Layer"] != 0:      
          if player == 0:
            move = self.moveTo(ship,((self.outerMapRadius()-1)*-1),0,locs, detonate) 
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
              ship.move(move[0], move[1])
              locs.append(move)
          else:
            move = self.moveTo(ship,self.outerMapRadius()-1, 0,locs, detonate) 
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
              ship.move(move[0],move[1])
              locs.append(move)
        else:
          self.moveAway(ship)
    return 1
    

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
      
  
      
