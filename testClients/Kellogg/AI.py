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
  
  def batShipControl(self,enemyListDict,myListDict):
    #Move towards enemy warp gate. if not in range of warp gate, attack enemy with most health that you can kill
    #once in range of warp gate, attack. if health is below x%, fire and self destruct
    warp = enemyListDict['Warp Gate'][0]
    for ship in myListDict['Battleship']:
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
      move = [0,0,0,0]
      for i in move:
        ship.move(ship.getX()-ship.getMaxMovement()/5,ship.getY()+ship.getMaxMovement()/2)
        if ship.getAttacksLeft()>0:
          ship.attack(ship)
              
  def supportControl(self,enemyListDict,myListDict):
    #if warpgate is below x health, move towards and heal warp Gate, else if wp in game,  move a support to them,  else move with largest cluster of friendly units
    target = myListDict['Warp Gate'][0]
    if myListDict['Warp Gate'][0].getHealth() <= myListDict['Warp Gate'][0].getMaxHealth()/2:
      for ship in myListDict['Support']:
          self.moveToTarget(myListDict['Support'][0],myListDict['Warp Gate'][0])
    
   # elif len(myListDict['Support'])>=2:
   #    if len(myListDict['Weapons Platform'])>0:
   #      self.moveToTarget(myListDict['Support'][0],myListDict['Weapons Platform'][0])
   #    for ship in myListDict['Support'][1:]:
   #      target2 = self.findCluster(ship,ship.getOwner(),myShips)
   #      if isinstance(target2,Ship) and target2.getType()!= 'Mine' and target2.getType()!='Support':
   #         target = target2
   #      self.moveToTarget(ship,target)
    else:
     for ship in myListDict['Support']:  
        target2 = self.findCluster(ship,ship.getOwner(),myShips)
        if isinstance(target2,Ship) and target2.getType() != 'Mine':# and target2.getType()!='Support':
          target = target2
        self.moveToTarget(ship,target)
           
  def empControl(self,enemyListDict,myListDict):
    #move towards largest cluster of enemy units, stun them. Works well with multi attackers
    target = enemyListDict['Warp Gate'][0]
    for ship in myListDict['EMP']:
      target2 = self.findCluster(ship,foePlayer[0].getId(),enemyShips)
      if isinstance(target2,Ship):
        target = target2
      self.moveToTarget(ship,target)
      foe = self.bestUseAttack(ship)
      if len(foe) > 0 and ship.getAttacksLeft()>0:
        ship.attack(ship)
                       
  def stealthControl(self,enemyListDict,myListDict):
  #stick with other stealth ships, move towards most isolated enemy, or target emps or other priority targets, swarm them, then flee
    for ship in myListDict['Stealth']:
      ship.move(ship.getX()+ship.getMaxMovement(),ship.getY())
         
  def cruiserControl(self,enemyListDict,myListDict):
    #mini battleship/big bomber
    for ship in myListDict['Cruisers']:
      ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()+2*ship.getMaxMovement()/3)
  
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
      ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()-2*ship.getMaxMovement()/3)
             
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
    if abs(dx)+abs(dy)>0 and ((ship.getX()+abs(dx))**2 + (ship.getX()+abs(dy))**2) <= self.mapRadius()**2:
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
                
  def moveInRange(self,ship,target):
#    maxMove = ship.getMaxMovement()
#    while maxMove > 0 and not inRange(ship.getX(),ship.getY(),ship.getRange(),target.getX(),target.getY(),target.getRadius):
    pass
  
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
     if abs(dx)+abs(dy)> 0 and totX + totY <= self.mapRadius()**2:
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
