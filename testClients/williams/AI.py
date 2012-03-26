#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

myShips = []
theirShips = []
shipHealth = {}
myMines = []
priorityList = {"Battleship" : 6.5,"Juggernaut" : 4,"Mine Layer" : 8.5,"Support" : 8, "Warp Gate" : 0, \
    "EMP" : 7,"Stealth" : 9,"Cruiser" : 3,"Weapons Platform" : 10,"Interceptor" : 1,"Bomber" : 2, "Mine" : -2}

#FEATURE LIST:
  #Optimize code      
  #Update all functions to new calls
  #Check logic for moving into mines
    
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
       
  def moveToInjured(self, ship, FriendlyWarpGate):
    weakestShip = myShips[0]
    for myShip in myShips:
      if (myShip.getHealth()/myShip.getMaxHealth())  <= (weakestShip.getHealth() / weakestShip.getMaxHealth()) and myShip.getId() != ship.getId() \
      and myShip.getType() != "Mine" and (myShip.getType() != "Warp Gate" or FriendlyWarpGate[0].getHealth() < 750):
        weakestShip = myShip
    move = self.moveTo(ship, weakestShip.getX(), weakestShip.getY())
    if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
      ship.move(move[0], move[1])  

  #Moves to nearest support ship if available
  def getHelp(self,ship, availShips): 
    if ship not in self.ships:
      return
    nearest = 1000
    nearestSupport = myShips[0]
    haveSupport = False
    if availShips["Support"] != 0:
      for myShip in myShips:
        if myShip.getType() == "Support" and self.distance(ship.getX(),myShip.getX(),ship.getY(),myShip.getY()) < nearest:
          haveSupport = True
          nearest = self.distance(ship.getX(),myShip.getX(),ship.getY(),myShip.getY())
          nearestSupport = myShip
    if haveSupport == True:
      move = self.moveTo(ship, nearestSupport.getX(), nearestSupport.getY())
      ship.move(move[0], move[1])
      return True
    else:
      return False
               
  #Returns the the furthest point along a path to target      
  def moveTo(self,ship,x,y):
    if ship not in self.ships:
      return [ship.getX(), ship.getY()]
    #Gets point furthest along a path between ship and target location
    distance = (((ship.getX() - x)**2) + ((ship.getY() - y)**2))**.5
    startDist = distance
    distRatio = 0
    range = 0
    #This is how far I can get and still attack their ship
    if ship.getType() == "Cruiser" or ship.getType() == "Battleship" or ship.getType() == "Bomber":
      range = ship.getRange() + 25
    if distance == 0:
      return [x,y]
    #Factoring my ships radius and my range
    #distance = distance - ship.getRadius() - ship.getRange()-30
    if ship.getType() == "Warp Gate":
      distRatio = ship.getRange() / distance
    else:
      if distance - ship.getRange() != 0:
        distRatio = ship.getMovementLeft() / (distance + ship.getRange())
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
        if self.getRange(finalX, finalY, ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
          goodMove = False
    #Check for friendly ships
    for myShip in myShips:
      #If a ship is there and has already moved this turn and isn't a mine, then it is a bad move
      if self.getRange(finalX, finalY, ship.getRadius(), myShip.getX(), myShip.getY(), myShip.getRadius()/2) \
      and myShip.getType() != "Mine" and myShip.getMovementLeft() != myShip.getMaxMovement():  
        goodMove = False
    if self.distance(0, finalX, 0, finalY) + ship.getRadius() > self.mapRadius:
      goodMove = False
    if ship.getType() == "Mine Layer":
      for mine in myMines:
        if self.getRange(finalX, finalY, 30, mine[0], mine[1], 30):
          goodMove = False 
          
    #If any of the above conditions are false, generate points in a circle around the ship
    #Otherwise, just move to that optimal location
    if goodMove == False:
      points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,32)
      if ship.getType() != "Mine Layer":
        points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,32))
        points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/3,24))
      distance = 10000
      #Iterate through all of these points to find which is the "best"
      for point in points:
        #Check to see if ship is within bounds of map
        if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.mapRadius:
          goodMove = True
          #Check for mines
          for enemy in theirShips:
            if enemy.getType() == "Mine":
              if self.getRange(point[0], point[1], ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
                goodMove = False
          #Check for friendly ships. 
          for myShip in myShips:
            #If a ship is there and has already moved this turn and isn't a mine, then it is a bad move
            if self.getRange(point[0], point[1], ship.getRadius(), myShip.getX(), myShip.getY(), myShip.getRadius()/2) \
            and myShip.getType() != "Mine" and myShip.getMovementLeft() != myShip.getMaxMovement():  
              goodMove = False
          #If a mine layer, make sure no mines are nearby
          if ship.getType() == "Mine Layer":
            for mine in myMines:
              if self.getRange(point[0], point[1], 30, mine[0], mine[1], 30):
                goodMove = False 
          #If all criteria met, check to see if this point is closer to target                
          if goodMove == True:
            if self.distance(point[0], x ,point[1], y) < distance and self.distance(point[0], x ,point[1], y) >= range:
              distance = self.distance(point[0], x , point[1], y)
              finalX = point[0]
              finalY = point[1]
              
    #If I have moved a lot, but only got a little bit closer I assume a mine is in the way.
    #If that is the case, find a path that ignores mines and move there    
    if (startDist - self.distance(finalX, x, finalY, y) < 0 and \
    self.distance(ship.getX(), finalX, ship.getY(), finalY) > ship.getMaxMovement()*.90 \
    and ship.getType() != "Mine Layer") or (ship.getMaxAttacks() == 0 and ship.getType() != "Warp Gate"):
      #print "It happened", ship.getId(), self.turnNumber, ship.getType()
      points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,32)
      points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,32))
      points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/3,24))
      for point in points:
        #Check to see if ship is within bounds of map
        if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.mapRadius:
          if self.distance(point[0], x ,point[1], y) < distance:
            distance = self.distance(point[0], x , point[1], y)
            finalX = point[0]
            finalY = point[1]        
    return [finalX, finalY]
   
  #Moves ship away from the nearest enemy
  def moveAway(self,ship): 
    if ship not in self.ships:
      return
    finalX = ship.getX()
    finalY = ship.getY()
    nearest = self.findNearest(ship)
    points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,32)
    points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,32))
    points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/3,24))
    distance = 0
    for point in points:
      if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.mapRadius:
        goodMove = True
        for enemy in theirShips:
          if enemy.getType() == "Mine":
            if self.getRange(point[0], point[1], ship.getRadius()+5, enemy.getX(), enemy.getY(), enemy.getRange()+5):  
              goodMove = False
        for myShip in myShips:
          #If a ship is there and has already moved this turn and isn't a mine, then it is a bad move
          if self.getRange(point[0], point[1], ship.getRadius()/2, myShip.getX(), myShip.getY(), myShip.getRadius()/2) \
          and myShip.getType() != "Mine" and myShip.getMovementLeft() != myShip.getMaxMovement():  
            goodMove = False
        if goodMove == True:
          if self.distance(point[0],nearest[0],point[1],nearest[1]) > distance:
            distance = self.distance(point[0],nearest[0],point[1],nearest[1])
            finalX = point[0]
            finalY = point[1]
    if self.distance(ship.getX(),finalX, ship.getY(),finalY) > 0:
      ship.move(finalX,finalY)
              
  #Spawn small ships until you reach input energy value
  def spawnSmall(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):
    if availShips["Bomber"] != 0 or availShips["Interceptor"] != 0:
      while self.players[player].getEnergy() > 30:
        if availShips["Bomber"] != 0:
          availShips["Bomber"].warpIn(agressiveWarp[0],agressiveWarp[1])
        if availShips["Interceptor"] != 0 and availShips["Battleship"] == 0:
          availShips["Interceptor"].warpIn(agressiveWarp[0],agressiveWarp[1])
        elif availShips["Interceptor"] != 0 and availShips["Battleship"] != 0 and availShips["Bomber"] != 0:
          pass
        else:
          return

  def spawnBig(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):   
    if availShips["Mine Layer"] != 0 and availShips["Weapons Platform"] != 0 and self.players[player].getEnergy() >= availShips["Weapons Platform"].getCost():
      availShips["Weapons Platform"].warpIn(safeWarp[0],safeWarp[1])
    elif availShips["Battleship"] != 0 and self.players[player].getEnergy() >= availShips["Battleship"].getCost():
      availShips["Battleship"].warpIn(agressiveWarp[0],agressiveWarp[1])
    elif (availShips["Interceptor"] != 0 or availShips["Bomber"] != 0) and availShips["Juggernaut"] != 0 and self.players[player].getEnergy() >= availShips["Juggernaut"].getCost():
      availShips["Juggernaut"].warpIn(agressiveWarp[0],agressiveWarp[1])
    elif availShips["Cruiser"] != 0 and self.players[player].getEnergy() >= availShips["Cruiser"].getCost():
      availShips["Cruiser"].warpIn(agressiveWarp[0],agressiveWarp[1])
    elif availShips["Weapons Platform"] != 0 and self.players[player].getEnergy() >= availShips["Weapons Platform"].getCost():
      availShips["Weapons Platform"].warpIn(safeWarp[0],safeWarp[1])

  def spawnSpecial(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):
    if self.players[player].getEnergy() >= 5:  
      if availShips["Mine Layer"] != 0:
        availShips["Mine Layer"].warpIn(defensiveWarp[0],defensiveWarp[1])
      if availShips["Support"] != 0 and self.players[player].getEnergy() >= 5:
        availShips["Support"].warpIn(agressiveWarp[0],agressiveWarp[1])
      elif availShips["EMP"] != 0 and self.players[player].getEnergy() >= 5:
        availShips["EMP"].warpIn(agressiveWarp[0],agressiveWarp[1]) 
      elif availShips["Stealth"] != 0 and self.players[player].getEnergy() >= 5:
        availShips["Stealth"].warpIn(agressiveWarp[0],agressiveWarp[1])

  def fillerSpawn(self, player, availShips, cheapest, safeWarp, defensiveWarp, agressiveWarp):    
    while self.players[player].getEnergy() >= cheapest and self.players[player].getEnergy() != 1:
      for type in availShips:
        if availShips[type] != 0 and availShips[type].getCost() <= self.players[player].getEnergy():
          availShips[type].warpIn(agressiveWarp[0],agressiveWarp[1])              
   
  def spawnShips(self, player, availShips, safeWarp, defensiveWarp, agressiveWarp):
    cheapest = 100
    for type in availShips:
      if availShips[type] != 0 and availShips[type].getCost() < cheapest:
        cheapest = availShips[type].getCost()
    self.spawnSmall(player, availShips, safeWarp, defensiveWarp, agressiveWarp)
    self.spawnSpecial(player, availShips, safeWarp, defensiveWarp, agressiveWarp)
    self.spawnBig(player, availShips, safeWarp, defensiveWarp, agressiveWarp)
    self.fillerSpawn(player, availShips, cheapest, safeWarp, defensiveWarp, agressiveWarp)
        
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
      return EnemyWarpGate[0]      
    
  #Attack all enemies in range with all attacks
  def attackAllInRange(self, ship, attackedList):
    if ship not in self.ships:
      return []
    #Create a list of things I've attacked and things I can attack
    #AttackedList will be used if multiple attack phases occur in one turn
    attackedList = attackedList
    attackList = []
    attacksLeft = ship.getAttacksLeft()
    #If EMP or Mine Layer only attack once per turn
    if (ship.getType() == "EMP" or ship.getType() == "Mine Layer") and ship.getAttacksLeft() > 0:
      hasAttacked = False
      for target in attackedList:
        if target.getId() == ship.getId():
          hasAttacked = True
      if hasAttacked == True:
        attacksLeft = 0
      else:
        attacksLeft = 1
    #Construct a list of all enemies in range
    for enemy in theirShips:
      #If in range and not a mine
      if self.getRange(ship.getX(),ship.getY(),ship.getRange(),enemy.getX(),enemy.getY(),enemy.getRadius()) and enemy.getType() != "Mine" \
      and enemy not in attackedList:
        attackList.append(enemy) 
    stacked = len(attackList)   
    if (ship.getType() == "EMP" or ship.getType() == "Mine Layer") and len(attackList) > 1 and attacksLeft > 0:
      ship.attack(ship)
      attackedList.append(ship)
      if ship.getType() == "Mine Layer":
        myMines.append([ship.getX(), ship.getY()])
    elif ship.getType() != "EMP" and ship.getType() != "Mine Layer":
      #While I still have targets and attacks, attack!
      while attacksLeft > 0 and len(attackList) > 0:
        target = self.highestPriorityEnemy(attackList)
        #If I have attacks, they have health left, and they are not mine => Attack them
        if attacksLeft > 0 and target.getHealth() > 0 and target.getOwner() != ship.getOwner():
          #If I killed them, remove them from list of possible targets
          ship.attack(target)
          attacksLeft = attacksLeft - 1
          attackList.remove(target)
          if target.getHealth() <= 0 and target.getId() in theirShips:
            theirShips.remove(target)
          else:
            attackedList.append(target)
        else:
          attackList.remove(target) 
    #If more than 5 enemies are stacked up, self destruct on them for massive damage! Awww yeah!         
    if stacked > 4 and (ship.getType() == "Bomber" or ship.getType() == "Interceptor"):
      #print stacked
      self.blowUp(ship)     
    return [attackedList]
    
  #Smart self-destruct. Moves to nearest enemy and then explodes
  def blowUp(self,ship):
    finalX = finalY = 0
    dest = self.findNearest(ship)
    points = self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()-5,64)
    points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/2,32))
    points.extend(self.pointsAtEdge(ship.getX(),ship.getY(),ship.getMovementLeft()/3,24))
    distance = 10000
    for point in points:
      if self.distance(0, point[0], 0, point[1]) + ship.getRadius() < self.mapRadius:            
        if self.distance(point[0], dest[0] ,point[1], dest[1]) < distance:
          distance = self.distance(point[0], dest[0] , point[1], dest[1])
          finalX = point[0]
          finalY = point[1]           
    if self.distance(ship.getX(), finalX, ship.getY(), finalY) <= ship.getMovementLeft():
      ship.move(finalX,finalY)
      if ship in self.ships:
        ship.selfDestruct()
        for enemy in theirShips:
          if self.getRange(ship.getX(),ship.getY(),ship.getRadius(), enemy.getX(), enemy.getY(), enemy.getRadius()):
            if enemy.getHealth() < 1:
              theirShips.remove(enemy)
      
              
  def init(self):      
    pass
    
  def end(self):
    pass    

  def run(self): 
    #Reset all of my globals
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
      if i.getId() == self.playerID:
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
    
    if player == 0:
      agressiveWarp = [FriendlyWarpGate[0].getX() + FriendlyWarpGate[0].getRange(), FriendlyWarpGate[0].getY()]
    else:
      agressiveWarp = [FriendlyWarpGate[0].getX() - FriendlyWarpGate[0].getRange(), FriendlyWarpGate[0].getY()]
    #Setting general warp locations   
    #Closest to enemy warpgate 
    #agressiveWarp = self.moveTo(FriendlyWarpGate[0], EnemyWarpGate[0].getX(), EnemyWarpGate[0].getY())   
    #Closest to far edge
   # safeWarp =  [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
    #if abs(safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier) > 500:
      #safeWarp = [430,0]
    #else:
      #safeWarp = [safeWarp[0]+FriendlyWarpGate[0].getRange()*modifier, 0]
    #Center of my warp gate   
    agressiveWarp = safeWarp = defensiveWarp = [FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY()]
         
    #Spawn my ships on the first turn
    if (self.turnNumber == 0 or self.turnNumber == 1) and self.playerID == player:
      self.spawnShips(player, availShips, safeWarp, defensiveWarp, agressiveWarp)
      
    defensiveCount = 0
      
    for ship in myShips:
      #If a ship is below 25% health, find the nearest enemy and self destruct
      alt = False
      if ship.getType() == "Mine Layer":
        unitInRange = False
        for enemy in theirShips:
          if self.getRange(ship.getX(), ship.getY(), ship.getRadius(), enemy.getX(), enemy.getY(), enemy.getRadius()):
            unitInRange = True
        if unitInRange == True:
          ship.selfDestruct()
      if ship.getHealth() <= (ship.getMaxHealth()*.25) and ship.getType() != "Warp Gate":
        self.attackAllInRange(ship, []) 
        self.blowUp(ship)
        alt = True
      elif ship.getHealth() > (ship.getMaxHealth()*.25) and ship.getHealth() < (ship.getMaxHealth()*.50) \
      and availShips["Support"] != 0 and ship.getType() != "Support":
        alt = self.getHelp(ship,availShips)
      #General ship type. Move to highest priority target and attack
      if alt == False:
        if ship.getType() == "Interceptor" or ship.getType() == "Bomber" or ship.getType() == "Cruiser" or \
        ship.getType() == "Juggernaut" or ship.getType() == "EMP" or ship.getType() == "Battleship" \
        or (ship.getType() == "Mine Layer" and defensiveCount > 1):
          #Try to attack everything in range    
          attackData = self.attackAllInRange(ship, [])
          #If all attacks expended, move away from enemies
          if ship.getAttacksLeft() == 0: 
            if ship.getType() != "EMP" and ship.getType() != "Mine Layer":
              self.moveAway(ship) 
            else:
              self.blowUp(ship)          
          #Move towards enemies and try to attack again          
          else:
            target = self.highestPriorityEnemy(theirShips)
            move = self.moveTo(ship,target.getX(),target.getY())
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
              ship.move(move[0],move[1])
            attacksLeft = self.attackAllInRange(ship, attackData[0]) 
            if ship.getMovementLeft() > 10:
              self.moveAway(ship) 
              
        #If I have mine layers, hide behind the field and fire, else move away from nearest enemy and attack          
        elif ship.getType() == "Weapons Platform": 
          if availShips["Mine Layer"] != 0:       
            if player == 0:
              move = self.moveTo(ship,((self.mapRadius-71)*-1), 0)          
              if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) < ship.getMovementLeft():
                ship.move(move[0], move[1])
            else:
              move = self.moveTo(ship,self.mapRadius-71, 0) 
              if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) < ship.getMovementLeft():
                ship.move(move[0],move[1])
          else:
            self.moveAway(ship)    
          self.attackAllInRange(ship, []) 
        #Move to the weakest ally 
        elif ship.getType() == "Support":
          self.moveToInjured(ship, FriendlyWarpGate)        
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
            move = self.moveTo(ship,target.getX(),target.getY())
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
              ship.move(move[0],move[1])
        #Defensive mine layers will place a mine field around the warp gate. Offensive will drop mines on enemies
        elif ship.getType() == "Mine Layer":
          defensiveCount += 1
          if ship.getAttacksLeft() > 0:
            move = self.moveTo(ship,FriendlyWarpGate[0].getX(), FriendlyWarpGate[0].getY())
            if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
              ship.move(move[0],move[1])
            if self.turnNumber >=4:                
              ship.attack(ship)
              myMines.append([ship.getX(), ship.getY()])                      
          else:
            self.blowUp(ship)
        #If I have mine layers, hide behind them. Otherwise move away from nearest enemy
        elif ship.getType() == "Warp Gate":  
          if availShips["Mine Layer"] != 0:      
            if player == 0:
              move = self.moveTo(ship,((self.mapRadius-71)*-1),0) 
              if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
                ship.move(move[0], move[1])
            else:
              move = self.moveTo(ship,self.mapRadius-71, 0) 
              if self.distance(ship.getX(), move[0], ship.getY(), move[1]) > 0 and self.distance(ship.getX(), move[0], ship.getY(), move[1]) <= ship.getMovementLeft():
                ship.move(move[0],move[1])
          else:
            self.moveAway(ship)
    return 1
    

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
      
  
      
