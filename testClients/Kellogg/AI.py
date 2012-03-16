#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

enemyShips = []
myPlayer = []
foePlayer = []
allTypes = ['Warp Gate', 'Battleship','Juggernaut', 'Mine Layer', 'Support', 'EMP', 'Stealth', 'Cruiser','Weapons Platform', 'Interceptor', 'Bomber','Mine']
myShips = []
numPoints = 720

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Kellogg"

  @staticmethod
  def password():
    return "password"

  def init(self):
    for pl in self.players:
      if self.playerID() == pl.getId():
        myPlayer.append(pl)
      else:
        foePlayer.append(pl)
    
  def warp(self,player,ships):
    warp = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Warp Gate":
        warp.append(ship)
    return warp
    
  def battleship(self,player,ships):
    battleship = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Battleship":
        battleship.append(ship)
    return battleship
    
  def juggernaut(self,player,ships):
    juggernaut = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Juggernaut":
        juggernaut.append(ship)
    return juggernaut
    
  def mineLays(self,player,ships):
    mines = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Mine Layer":
        mines.append(ship)
    return mines  

  def support(self,player,ships):
    support = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Support":
        support.append(ship)
    return support

  def emp(self,player,ships):
    emp = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "EMP":
        emp.append(ship)
    return emp
        
  def stealth(self,player,ships):
    stealth = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Stealth":
        stealth.append(ship)
    return stealth
    
  def cruiser(self,player,ships):
    cruiser = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Cruiser":
        cruiser.append(ship)
    return cruiser

  def weapons(self,player,ships):
    weapons = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Weapons Platform":
        weapons.append(ship)
    return weapons
    
  def interceptor(self,player,ships):
    intercept = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Interceptor":
        intercept.append(ship)
    return intercept

  def bomber(self,player,ships):
    bomber = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Bomber":
        bomber.append(ship)
    return bomber
         
  def mines(self,player,ships):
    mines = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Mine":
        mines.append(ship)
    return mines
  
  def warpControl(self,enemyListDict,myListDict):
    for w in myListDict['Warp Gate']:
      self.smartWarp(w)
      nearest = self.findNearest(w,enemyShips)
      self.moveAway(w,nearest)
#      self.moveTo(w,w.getX(),w.getY(),nearest.getX(),nearest.getY(),w.getMaxMovement(),"toward")
  
  def batShipControl(self,enemyListDict,myListDict):
    #Move towards enemy warp gate. if not in range of warp gate, attack enemy with most health that you can kill
    #once in range of warp gate, attack. if health is below x%, fire and self destruct
    warp = enemyListDict['Warp Gate'][0]
    for ship in myListDict['Battleship']:
#      self.moveTo(ship,ship.getX(),ship.getY(),warp.getX(),warp.getY(),ship.getMaxMovement(),"toward")
      self.moveToTarget(ship,warp)
      if self.inRange(ship.getX(),ship.getY(),ship.getRange(),warp.getX(),warp.getY(),warp.getRadius()):
        ship.attack(warp)
      else:
        target = self.bestUseAttack(ship)
        if len(target) > 0:
          ship.attack(target[0])
  
  def juggControl(self,enemyListDict,myListDict):
    #move towards largest cluster of enemies within a distance equal to attack range, attack each enemy, if you have attacks left, start
    #towards new cluster, if you have movement left, move to relative safety, if not paired with an emp
    for ship in myListDict['Juggernaut']:
      ship.move(ship.getX()-ship.getMaxMovement()/2,ship.getY()-ship.getMaxMovement()/2)

  def mineLayerControl(self,enemyListDict,myListDict):
  #create mine field around warp gate, if x amount of mines already near warp gate and have mines left, move towards
  #largest cluster dropping mines 
    for ship in myListDict['Mine Layer']:
      ship.move(ship.getX()-ship.getMaxMovement()/5,ship.getY()+ship.getMaxMovement()/2)
      if ship.getAttacksLeft()>0:
        ship.attack(ship)
              
  def supportControl(self,enemyListDict,myListDict):
    #if warpgate is below x health, move towards and heal warp Gate, else if wp in game,  move a support to them,  else move with largest cluster of friendly units
    target = myListDict['Warp Gate'][0]
    if myListDict['Warp Gate'][0].getHealth() <= myListDict['Warp Gate'][0].getMaxHealth()/2:
      for ship in myListDict['Support']:
#          self.moveTo(ship,ship.getX(),ship.getY(),target.getX(),target.getY(),target.getMaxMovement(),"toward")
          self.moveToTarget(ship,target)
    else:
     for ship in myListDict['Support']:  
        target2 = self.findCluster(ship,ship.getOwner(),myShips)
        if isinstance(target2,Ship) and target2.getType() != 'Mine':# and target2.getType()!='Support':
          target = target2
#        self.moveTo(ship,ship.getX(),ship.getY(),target.getX(),target.getY(),target.getMaxMovement(),"toward")
        self.moveToTarget(ship,target)
           
  def empControl(self,enemyListDict,myListDict):
    #move towards largest cluster of enemy units, stun them. Works well with multi attackers
    target = enemyListDict['Warp Gate'][0]
    for ship in myListDict['EMP']:
      target2 = self.findCluster(ship,foePlayer[0].getId(),enemyShips)
      if isinstance(target2,Ship):
        target = target2
#      self.moveTo(ship,ship.getX(),ship.getY(),target.getX(),target.getY(),target.getMaxMovement(),"toward")
      self.moveToTarget(ship,target)
      foe = self.bestUseAttack(ship)
      if len(foe) > 0 and ship.getAttacksLeft()>0:
        ship.attack(ship)
                       
  def stealthControl(self,enemyListDict,myListDict):
  #stick with other stealth ships, move towards most isolated enemy, or target emps or other priority targets, swarm them, then flee
    for ship in myListDict['Stealth']:
      nearest = self.findNearest(ship,enemyShips)
      self.moveToTarget(ship,nearest)
      target = self.bestUseAttack(ship)
      if len(target) > 0:
        ship.attack(target[0])
      
         
  def cruiserControl(self,enemyListDict,myListDict):
    #mini battleship/big bomber
    for ship in myListDict['Cruisers']:
      nearest = self.findNearest(ship,enemyShips)
      self.moveToTarget(ship,nearest)
      target = self.bestUseAttack(ship)
      if len(target) > 0:
        ship.attack(target[0])
  
  def weapPlatControl(self,enemyListDict,myListDict):
    #stay far from enemy units, snipe priority targets (emp,stealth, etc)
    #TODO make attacking more efficient
    for ship in myListDict['Weapons Platform']:
      attacks = ship.getMaxAttacks()
      if attacks > 0:
        for support in enemyListDict['Support']:
          ship.attack(support)
          attacks-=1
      if attacks > 0:
        for wp in enemyListDict['Weapons Platform']:
          ship.attack(wp)
          attacks-=1
      if attacks > 0:
        for miner in enemyListDict['Mine Layer']:
         if miner.getAttacksLeft()>0:
           ship.attack(miner)
           attacks-=1
      if attacks > 0:
        for stealth in enemyListDict['Stealth']:
          ship.attack(stealth)
          attacks -= 1
      if attacks > 0:
          ship.attack(enemyListDict['Warp Gate'][0])
      #TODO make it so they attack anything that is shooting them
      nearest = self.findNearest(ship,enemyShips)
      self.moveAway(ship,nearest)

  def intercepControl(self,enemyListDict,myListDict):
  #mini juggernauts,
    for ship in myListDict['Interceptor']:
      ship.move(ship.getX()-2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
           
  def bomberControl(self,enemyListDict,myListDict):
    #attack stuff 
    for ship in myListDict['Bomber']:
      nearest = self.findNearest(ship,enemyShips)
      self.moveToTarget(ship,nearest)
      target = self.bestUseAttack(ship)
      if len(target) > 0:
        ship.attack(target[0])
             
  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  #takes a source (ship) and side (0 or 1). Finds all ships on the side given in range, returns a list of the ships    
  def allInRange(self, source, side, range):
    result = []
    for ship in self.ships:
      if ship.getType()!= 'Mine':
        if ship.getOwner() == side and self.inRange(source.getX(), source.getY(), range, ship.getX(), ship.getY(), ship.getRadius()):
          result.append(ship)
    return result
  
  def moveToTarget(self,ship,target):
    maxMove = ship.getMaxMovement()
    dx = target.getX()-ship.getX()
    dy = target.getY()-ship.getY()
    dist = abs(dx)+abs(dy)
    if dist > maxMove:
      dx = int(math.copysign(maxMove/2,dx))
      dy = int(math.copysign(maxMove/2,dy))
    if abs(dx)+abs(dy)>0 and ((ship.getX()+abs(dx))**2 + (ship.getX()+abs(dy))**2) <= self.outerMapRadius()**2:
      ship.move(ship.getX()+dx,ship.getY()+dy)
    maxMove-=dist
    
  #takes a seeker (Ship that's trying to find group, a side (whose ships you're looking to find a group of) and a list of ships to look through
  #returns the ship that has the ships in your effective range
  def findCluster(self,seeker,side,ships):
    groupSize = 0
    for ship in ships:
      currentSize = len(self.allInRange(ship,side,seeker.getRange()))
      if currentSize > groupSize:
        groupSize = currentSize
        centerShip = ship
    return centerShip
  
  def findNearest(self,source,ships):
    distance = 200000
    for ship in ships:
      currentDist = self.distance(source.getX(),ship.getX(),source.getY(),ship.getY())
      if currentDist < distance:
        distance = currentDist
        target = ship    
    return target
                
  def moveTo(self,ship,fromX,fromY,toX,toY,movement,direction):
      if direction == "toward":
        dx = toX-fromX; dy = toY-fromY
      elif direction == "away":
        dx = fromX-toX; dy = fromY-toY
        
      while movement > 0 and abs(toX-fromX)+abs(toY-fromY)>0:
        if abs(dx+dy)>movement:
          dx/=2
          dy/=2
  #        print "halving dx,dy, movement ",dx,dy,movement
          if dx == -1 and dy == -1 and movement == 1:
            break
        else:
            newX = fromX+dx; newY = fromY+dy
            if int(math.sqrt(newX**2+newY**2)) < self.innerMapRadius():
              print "moving out of inner"
              newX,newY = self.farthestPoint(0,0,movement,self.innerMapRadius(),fromX,fromY,"outer")
              movement-=abs(fromX-newX)+abs(fromY-newY);fromX=newX; fromY=newY; 
              ship.move(newX,newY)
            elif int(math.sqrt(newX**2+newY**2)) > self.outerMapRadius():
              print "moving inside of outer"
              newX,newY = self.farthestPoint(0,0,movement,self.outerMapRadius(),fromX,fromY,"inner")
              fromX=newX; fromY=newY; movement-=abs(fromX-newX)+abs(fromY-newY)
              ship.move(newX,newY)
            else:
              mines = self.mines(ship.getOwner()^1,enemyShips)
              if len(mines)>0:
                for mine in mines:
                  if self.inRange(fromX,fromY,ship.getRadius(),mine.getX(),mine.getY(),mine.getRange()):
#                  if abs(fromX-mine.getX())+abs(fromY-mine.getY())<=(ship.getRadius()+mine.getRange()):
                    print "avoiding mines"
                    newX,newY = self.farthestPoint(mine.getX(),mine.getY(),movement,mine.getRange(),fromX,fromY)
                    fromX=newX; fromY=newY; movement-=abs(fromX-newX)+abs(fromY-newY)
                    ship.move(newX,newY)                           
                  else:
#                    print "easy move"
                    ship.move(newX,newY)
                    fromX+=dx; fromY+=dy
                    movement -=abs(dx+dy)
              else: 
 #               print "from moveTo, newX,newY",newX,newY
                ship.move(newX,newY)
                fromX+=dx; fromY+=dy
                movement -=abs(dx+dy)
                                                                         
  
  def moveAway(self,ship,target):
     maxMove = ship.getMaxMovement()
     dx = ship.getX()-target.getX()
     dy = ship.getY()-target.getY()
     dist = abs(dx)+abs(dy)
     if dist > maxMove:
       dx = int(math.copysign(maxMove/2,dx))
       dy = int(math.copysign(maxMove/2,dy))
     totX = (ship.getX()+dx)**2
     totY = (ship.getY()+dy)**2
     if abs(dx)+abs(dy)> 0 and totX + totY <= self.outerMapRadius()**2:
       ship.move(ship.getX()+dx,ship.getY()+dy)
       maxMove-=dist
                                              
  def testWarp(self,warpShip):
     typeDict = {}
     for type in self.shipTypes:
       typeDict[type.getType()] = type
     energy = myPlayer[0].getEnergy()
     if 'Support' in typeDict:
       while energy >= typeDict['Support'].getCost():
         typeDict['Support'].warpIn(warpShip.getX(),warpShip.getY())                      
         energy-=typeDict['Support'].getCost()
            
  def smartWarp(self,warpShip):
     #TODO: make smarterer
     #dictionaries are great
     typeDict = {}
     for type in self.shipTypes:
       typeDict[type.getType()] = type
     energy = myPlayer[0].getEnergy()
     sortedCost = sorted(self.shipTypes, key=lambda x: x.getCost())
     minCost = sortedCost[0].getCost()
     if 'Weapons Platform' in typeDict and energy >= typeDict['Weapons Platform'].getCost():
       typeDict['Weapons Platform'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Weapons Platform'].getCost()
       if  energy >= typeDict['Weapons Platform'].getCost():
         typeDict['Weapons Platform'].warpIn(warpShip.getX(),warpShip.getY())
         energy-=typeDict['Weapons Platform'].getCost()
     if 'Support' in typeDict and energy >= typeDict['Support'].getCost():
       typeDict['Support'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Support'].getCost()
       if  energy >= typeDict['Support'].getCost():
         typeDict['Support'].warpIn(warpShip.getX(),warpShip.getY())
         energy-=typeDict['Support'].getCost()
     if 'Mine Layer' in typeDict and energy >= typeDict['Mine Layer'].getCost():
       typeDict['Mine Layer'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Mine Layer'].getCost()
       if energy >= typeDict['Mine Layer'].getCost():
         typeDict['Mine Layer'].warpIn(warpShip.getX(),warpShip.getY())
         energy-=typeDict['Mine Layer'].getCost()
     if 'Battleship' in typeDict and energy >= typeDict['Battleship'].getCost():
       typeDict['Battleship'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Battleship'].getCost()
     elif 'Juggernaut' in typeDict and energy >= typeDict['Juggernaut'].getCost():
       typeDict['Juggernaut'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Juggernaut'].getCost()
     elif 'Cruiser' in typeDict and energy >= typeDict['Cruiser'].getCost():
       typeDict['Cruiser'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['Cruiser'].getCost()          
     if 'EMP' in typeDict and energy >= typeDict['EMP'].getCost():
       typeDict['EMP'].warpIn(warpShip.getX(),warpShip.getY())
       energy-=typeDict['EMP'].getCost()
     while energy >= minCost:
       print energy
       if 'Stealth' in typeDict and energy >= typeDict['Stealth'].getCost():
        typeDict['Stealth'].warpIn(warpShip.getX(),warpShip.getY())
        energy-=typeDict['Stealth'].getCost()
       elif 'Bomber' in typeDict and energy >= typeDict['Bomber'].getCost():
         typeDict['Bomber'].warpIn(warpShip.getX(),warpShip.getY())
         energy-=typeDict['Bomber'].getCost()
       elif 'Interceptor' in typeDict and energy >= typeDict['Interceptor'].getCost():
         typeDict['Interceptor'].warpIn(warpShip.getX(),warpShip.getY())
         energy-=typeDict['Interceptor'].getCost()
       else:
         break
     return                                                                   
              
#TODO have it return a list, or take a list of attackable targets                                                                                                                                                                                                                                                                                     
  #goes through all enemies in range, and returns the a list of the enemy whose current health is closest to, but less than, that ships damage. 
  #If no such enemy fits this (i.e., no enemey has less health than damage), returns a list of the enemy with lowest health
  def bestUseAttack(self,ship):
    foe = ship.getOwner()^1
    targets = self.allInRange(ship,foe,ship.getRange())
    result = []
    if len(targets) > 0:
      health = 0
      damage = ship.getDamage()
      aNewList = sorted(targets, key=lambda x: x.getHealth())
      print aNewList
      guy = aNewList[0]    
      result.append(aNewList[0])
      for target in targets:
        if target.getHealth() > health and target.getHealth() <= damage:# and target.getMaxHealth() > maxHealth:
          result.append(target)
          guy = target
          health = target.getHealth()
    #result.append(guy) 
#      print "OUTPUT FROM RESULT LOOKEY HERE-------------------------------------"
      for r in result:
        print r.getHealth()
      result.sort()
      result.reverse()
      sortHealth = [s.getHealth() for s in result]
#      print "RESULT = ",sortHealth
    return result
    
    
  def seppuku(self,ship):
    if ship.getHealth() <= ship.getMaxHealth()/3 or ship.getMaxAttacks() == 0:
      if ship.getType()!= 'Warp Gate':
        target = self.findNearest(ship,enemyShips)
        self.moveToTarget(ship,target)
        ship.selfDestruct()
    return 
  
  def findInnerPoints(self,centerX,centerY,radius,n):
      radius-=radius/10
      pi = 3.1415926535897932384626433832795028841971693993751058209
      Xval = [(int(math.floor((centerX + math.cos(2*pi/n*x)*radius)))) for x in range(0,n+1)]
      Yval = [(int(math.floor((centerY + math.sin(2*pi/n*y)*radius)))) for y in range(0,n+1)]
      return Xval,Yval
                                
  def findOuterPoints(self,centerX,centerY,radius,n):
      radius+=radius/10
      pi = 3.1415926535897932384626433832795028841971693993751058209 
      #angles = [0,pi/6,pi/4,pi/3,pi/2,2*pi/3,3*pi/4,5*pi/6,pi,7*pi/6,5*pi/4,4*pi/3,3*pi/2,5*pi/3,7*pi/4,11*pi/6]
      Xval = [(int(math.floor((centerX + math.cos(2*pi/n*x)*radius)))) for x in range(0,n+1)]
#      Xval = []
      Yval = [(int(math.floor((centerY + math.sin(2*pi/n*y)*radius)))) for y in range(0,n+1)]
#      Yval = []
#      for i in angles:
#        Xval.append(centerX+radius*math.cos(i))
#        Yval.append(centerY+radius*math.sin(i))
#        print "HERE ARE THE POINTS ",centerX,centerY,radius,i,math.cos(i)
#        print centerX+radius*math.cos(i)
#        print centerY+radius*math.sin(i)
      return Xval,Yval      
  
  def farthestPoint(self,centerX,centerY,movement,radius,shipX,shipY,where):
    print "calling Farthest Point"
    if where == "outer":
      xPoints,yPoints = self.findOuterPoints(centerX,centerY,radius,numPoints)
    elif where == "inner":
      xPoints,yPoints = self.findInnerPoints(centerX,centerY,radius,numPoints) 
      
    distance = 0
    for i in range(len(xPoints)):
      xP = int(xPoints[i]); yP = int(yPoints[i])
      newDis = self.distance(shipX,centerX+xP,shipY,centerY+yP)
      #print "xP,yP",xP,yP,"newDis",newDis,"movement",movement,"x,y",shipX,shipY
     # print "NEW DISTANCE",newDis
      #Ydis = abs(shipX-math.sqrt((centerX+xP)**2))
      #Ydis = abs(shipY-math.sqrt((centerY+yP)**2))
#      print "shipX,shipY",shipX,shipY,"Xdis,Ydis",Xdis,Ydis,"movment",movement
#      print "center x is",centerX,"center y is",centerY,"xP is",xP,"yP is",yP,"travel distance is", abs(shipX-(centerX+xP)) + abs(shipY-(centerY+yP)), "compared to current distance",distance,"movement is",movement
      if newDis >= distance and newDis <= movement:
      #if abs(shipX-(centerX+xP)) + abs(shipY-(centerY+yP)) > distance and abs(shipX-(centerX+xP)) + abs(shipY-(centerY+yP)) <= movement:
        newX = xP
        newY = yP
        distance = newDis
#        print "setting distance to ",distance
#    print "newX,newY",newX,newY
    return newX,newY
    
#  def checkMove(self,ship,x,y,movement):
#    if x**2 + y**2 < self.innerMapRadius():
#      newX,newY = self.farthesPoint(x,y,movement,self.innerMapRadius())
#      movement-=abs(x-newX)+abs(y-newY)
#      ship.move(newX,newY)
#      return False
#    elif x**2 + y**2 > self.outerMapRadius():
#      newX,newY = self.farthestPoint(x,y,movement,self.outerMapRadius())
#      movement-=abs(x-newX)+abs(y-newY)
#      ship.move(newX,newY)
#      return False
#    mines = self.mines(ship.getOwner()^1,enemyShips)
#    for mine in mines:
#      if abs(x-mine.getX())+abs(y-mine.getY())<=(ship.getRadius()+mine.getRange()):
#        newX,newY = self.farthesPoint(x,y,movement,mine.getRange())
#        movement-=abs(x-newX)+abs(y-newY)
#        ship.move(newX,newY)
#        return False
#    return True
  
  def run(self):
    #Gah, so many ships
    types=[]; warps=[]; batShips=[]; juggs=[]; mineLayers=[]; supports=[]; mines = []
    emps=[]; stealths=[]; cruisers=[]; weapPlats=[]; interceps=[]; bombers=[];
    
    foewarps=[]; foebatShips=[]; foejuggs=[]; foemineLayers=[]; foesupports=[]; foemines = []
    foeemps=[]; foestealths=[]; foecruisers=[]; foeweapPlats=[]; foeinterceps=[]; foebombers=[];
       
    del enemyShips[0:len(enemyShips)]
    del myShips[0:len(myShips)]
        
    #get string of each ship type
    for type in self.shipTypes:
      types.append(type.getType())
    types+=['Warp Gate']  
    if 'Mine Layer' in types:
      types+=['Mines']
    
    for ship in self.ships:
      if ship.getOwner() == foePlayer[0].getId():
        enemyShips.append(ship)
      if ship.getOwner() == myPlayer[0].getId():
        myShips.append(ship)
    
    #dictionary magic
    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mineLays,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber,'Mine':self.mines}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interceps,'Bomber':bombers,'Mine':mines}
    enemyListDict ={'Warp Gate':foewarps,'Battleship':foebatShips,'Juggernaut':foejuggs,'Mine Layer':foemineLayers,'Support':foesupports,'EMP':foeemps,'Stealth':foestealths,'Cruiser':foecruisers,'Weapons Platform':foeweapPlats,'Interceptor':foeinterceps,'Bomber':foebombers,'Mine':foemines}
    controlDict = {'Warp Gate':self.warpControl,'Battleship':self.batShipControl,'Juggernaut':self.juggControl,'Mine Layer':self.mineLayerControl,'Support':self.supportControl,'EMP':self.empControl,'Stealth':self.stealthControl,'Cruiser':self.cruiserControl,'Weapons Platform':self.weapPlatControl,'Interceptor':self.intercepControl,'Bomber':self.bomberControl}
	
    for ty in types:
      try:
        myListDict[ty] = funDict[ty](myPlayer[0].getId(),self.ships)  
        enemyListDict[ty] = funDict[ty](foePlayer[0].getId(),self.ships)
      except KeyError:
        pass #print ty
   
    for ty in myListDict:
       try:
         controlDict[ty](enemyListDict,myListDict)
       except KeyError:
         pass #print ty
    
    #end dictionary magic
    
    for ship in myShips:
      self.seppuku(ship)

    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
