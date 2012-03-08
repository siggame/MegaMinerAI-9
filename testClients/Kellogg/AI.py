#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

enemyShips = []
myPlayer = []
foePlayer = []
allTypes = ['Warp Gate', 'BattleShip','Juggernaut', 'Mine Layer', 'Support', 'EMP', 'Stealth', 'Cruiser','Weapons Platform', 'Interceptor', 'Bomber','Mines']
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
    
  def mines(self,player,ships):
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
  
  def warpControl(self,warps,enemyListDict,myListDict):
    for w in myListDict['Warp Gate']:
#      w.move(w.getX()+10,w.getY()-10)
      for type in self.shipTypes:
        if type.getType() == 'Battleship':
          type.warpIn(w.getX(),w.getY())
      self.smartWarp(w)
  
  def batShipControl(self,batShips,enemyListDict,myListDict):
    #Move towards enemy warp gate. if not in range of warp gate, attack enemy with most health that you can kill
    #once in range of warp gate, attack. if health is below x%, fire and self destruct
    warp = enemyListDict['Warp Gate'][0]
    for ship in batShips:
      print "CONTROLLING BATSHIPS"
      self.moveToTarget(ship,warp)
      if self.inRange(ship.getX(),ship.getY(),ship.getRange(),warp.getX(),warp.getY(),warp.getRadius()):
        ship.attack(warp)
      else:
        target = self.bestUseAttack(ship)
        if len(target) > 0:
          ship.attack(target[0])
  
  def juggControl(self,juggs,enemyListDict,myListDict):
    #move towards largest cluster of enemies within a distance equal to attack range, attack each enemy, if you have attacks left, start
    #towards new cluster, if you have movement left, move to relative safety, if not paired with an emp
    pass
#    for ship in juggs:
#      ship.move(ship.getX()-ship.getMaxMovement()/2,ship.getY()-ship.getMaxMovement()/2)

  def mineLayerControl(self,mineLayers,enemyListDict,myListDict):
  #create mine field around warp gate, if x amount of mines already near warp gate and have mines left, move towards
  #largest cluster dropping mines 
   pass
#    for ship in mineLayers:
#      ship.move(ship.getX()-ship.getMaxMovement()/5,ship.getY()+ship.getMaxMovement()/2)
#      if ship.getAttacksLeft()>0
#        ship.attack(ship)
              
  def supportControl(self,supports,enemyListDict,myListDict):
    #if warpgate is below x health, move towards and heal warp Gate, else move with largest cluster of friendly units
    target = myListDict['Warp Gate'][0]
    for ship in supports:
      if myListDict['Warp Gate'][0].getHealth() <= myListDict['Warp Gate'][0].getMaxHealth()/2:
        self.moveToTarget(ship,myListDict['Warp Gate'][0]) 
      else:
        target2 = self.findCluster(ship,ship.getOwner(),myShips)
        if isinstance(target2,Ship):
          target = target2
        self.moveToTarget(ship,target)
      ship.move(ship.getX()+10,ship.getY()+10)      
           
  def empControl(self,emps,enemyListDict,myListDict):
    #move towards largest cluster of enemy units, stun them. Works well with multi attackers
    target = enemyListDict['Warp Gate'][0]
    for ship in emps:
      target2 = self.findCluster(ship,foePlayer[0].getId(),enemyShips)
      if isinstance(target2,Ship):
        target = target2
      print target.getType()
      self.moveToTarget(ship,target)
      foe = self.bestUseAttack(ship)
      if len(foe) > 0 and ship.getAttacksLeft()>0:
        ship.attack(ship)
                       
  def stealthControl(self,stealths,enemyListDict,myListDict):
  #stick with other stealth ships, move towards most isolated enemy, or target emps or other priority targets, swarm them, then flee
    pass
#    for ship in stealths:
#      ship.move(ship.getX()+ship.getMaxMovement(),ship.getY())
         
  def cruiserControl(self,cruisers,enemyListDict,myListDict):
    #mini battleship/big bomber
    pass
    #for ship in cruisers:
     # ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()+2*ship.getMaxMovement()/3)
  
  def weapPlatControl(self,weapPlats,enemyListDict,myListDict):
    #stay far from enemy units, snipe priority targets (emp,stealth, etc)
    pass
    #for ship in weapPlats:
    #  ship.move(ship.getX()+2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
  
  def intercepControl(self,interceps,enemyListDict,myListDict):
  #mini juggernauts,
    pass
#    for ship in interceps:
#      ship.move(ship.getX()-2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
           
  def bomberControl(self,bombers,enemyListDict,myListDict):
    #attack stuff 
    pass
 #   for ship in bombers:
 #     ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()-2*ship.getMaxMovement()/3)
             
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
      dx = int(math.copysign(maxMove/3,dx))
      dy = int(math.copysign(maxMove/3,dy))
    if abs(dx)+abs(dy)>0:
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
  
  def findNearest(self,ship,ships):
    pass
                
  def moveInRange(self,ship,target):
    maxMove = ship.getMaxMovement()
#    while maxMove > 0 and not inRange(ship.getX(),ship.getY(),ship.getRange(),target.getX(),target.getY(),target.getRadius):
    pass
  
  def moveOutRange(self,ship,target):
    pass
  
  def smartWarp(self,warpShip):
     #TODO: make smarter
     warping = []
     for player in self.players:
       if self.playerID() == player.getId():
         myPlayer = player
     shipTypes = self.shipTypes
     types = []
     sortedCost = sorted(shipTypes, key=lambda x: x.getCost())
     minCost = sortedCost[0].getCost()
     for type in shipTypes:
       types.append(type.getType())
     energy = myPlayer.getEnergy()
     while energy >= minCost:
       if 'Battleship' in types:
         for type in shipTypes:
           if type.getType() == 'BattleShip' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       elif 'Juggernaut' in types:
         for type in shipTypes:
           if type.getType() == 'Juggernaut' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       if 'Mine Layer' in types:
         for type in shipTypes:
           if type.getType() == 'Mine Layer' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       if 'Support' in types:
         for type in shipTypes:
           if type.getType() == 'Support' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       if 'EMP' in types:
          for type in shipTypes:
            if type.getType() == 'EMP' and energy >= type.getCost():
              warping.append(type)
              energy-=type.getCost()
       if 'Stealth' in types:
         for type in shipTypes:
           if type.getType() == 'Stealth' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       if 'Cruiser' in types:
          for type in shipTypes:
            if type.getType() == 'Cruiser' and energy >= type.getCost():
              warping.append(type)
              energy-=type.getCost()
       if 'Weapons Platforms' in types:
          for type in shipTypes:
            if type.getType() == 'Weapons Platform' and energy >= type.getCost():
              warping.append(type)
              energy-=type.getCost()
       if 'Interceptor' in types:
         for type in shipTypes:
           if type.getType() == 'Interceptor' and energy >= type.getCost():
             warping.append(type)
             energy-=type.getCost()
       if 'Bomber' in types:
         for type in shipTypes:
           if type.getType() == 'Bomber' and energy >= type.getCost():
            warping.append(type)
            energy-=type.getCost()
     
     for type in warping:
       type.warpIn(warpShip.getX(),warpShip.getY())
     return
                                                                                                                                                                                                                                                                                     
  #goes through all enemies in range, and returns the a list of the enemy whose current health is closest to, but less than, that ships damage. 
  #If no such enemy fits this (i.e., no enemey has less health than damage), returns a list of the enemy with lowest health
  def bestUseAttack(self,ship):
    foe = ship.getOwner()^1
    targets = self.allInRange(ship,foe,ship.getRange())
    result = []
    if len(targets)>0:
      health = 0
      damage = ship.getDamage()
      aNewList = sorted(targets, key=lambda x: x.getHealth())
      guy = aNewList[0]    
      for target in targets:
        if target.getHealth() > health and target.getHealth() <= damage:# and target.getMaxHealth() > maxHealth:
          guy = target
          health = target.getHealth()
      result.append(guy) 
    return result
    
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
    if 'Mine Layers' in types:
      types+=['Mines']
    
    for ship in self.ships:
      if ship.getOwner() == foePlayer[0].getId():
        enemyShips.append(ship)
      if ship.getOwner() == myPlayer[0].getId():
        myShips.append(ship)
    
    #dictionary magic
    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mines,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber,'Mines':self.mines}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interceps,'Bomber':bombers,'Mines':mines}
    enemyListDict ={'Warp Gate':foewarps,'Battleship':foebatShips,'Juggernaut':foejuggs,'Mine Layer':foemineLayers,'Support':foesupports,'EMP':foeemps,'Stealth':foestealths,'Cruiser':foecruisers,'Weapons Platform':foeweapPlats,'Interceptor':foeinterceps,'Bomber':foebombers,'Mines':foemines}
    controlDict = {'Warp Gate':self.warpControl,'Battleship':self.batShipControl,'Juggernaut':self.juggControl,'Mine Layer':self.mineLayerControl,'Support':self.supportControl,'EMP':self.empControl,'Stealth':self.stealthControl,'Cruiser':self.cruiserControl,'Weapons Platform':self.weapPlatControl,'Interceptor':self.intercepControl,'Bomber':self.bomberControl}
	
    for ty in types:
      try:
        myListDict[ty] = funDict[ty](myPlayer[0].getId(),self.ships)  
        enemyListDict[ty] = funDict[ty](foePlayer[0].getId(),self.ships)
      except KeyError:
        pass #print ty
   
    for ty in myListDict:
       try:
         controlDict[ty](myListDict[ty],enemyListDict,myListDict)
       except KeyError:
         pass #print ty
    #for ty in types:
    #  for ship in myListDict[ty]:
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
