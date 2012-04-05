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
numPoints = 100
closingPoints = 20
typePriority = ['Mine','Support','Stealth','Battleship','Weapons Platform','Mine Layer','Cruiser','Bomber','EMP','Interceptor','Juggernaut','Warp Gate']

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
      if self.playerID == pl.getId():
        myPlayer.append(pl)
      else:
        foePlayer.append(pl)
    
  def typeList(self,player,ships,type):
    list = []
    for ship in self.ships:
      if ship.getOwner() == player and ship.getType() == type:
        list.append(ship)
    return list
  
  def warpControl(self,myListDict,enemyListDict):
    for w in myListDict['Warp Gate']:
      self.smartWarp(w)
      nearest = self.findNearest(w,enemyShips)
      self.moveAway(w,nearest,enemyListDict['Mine'])
  
  def batShipControl(self,myListDict,enemyListDict):
    #Move towards enemy warp gate. if not in range of warp gate, attack enemy with most health that you can kill
    #once in range of warp gate, attack. if health is below x%, fire and self destruct
    print "bat",enemyListDict['Warp Gate']
    if len(enemyListDict['Warp Gate'])>0:
      warp = enemyListDict['Warp Gate'][0]
    for ship in myListDict['Battleship']:
      self.smartMoveTo(ship,warp,enemyListDict)
      if self.inRange(ship.getX(),ship.getY(),ship.getRange(),warp.getX(),warp.getY(),warp.getRadius()):
        ship.attack(warp)
      else:
        self.smartAttack(ship,enemyListDict,self.ships)
#        target = self.bestUseAttack(ship,enemyShips)
#        if isinstance(target,Ship):
#          ship.attack(target)
#          if target.getHealth()<1 and target in enemyShips:
#            enemyShips.remove(target)
  
  def juggControl(self,myListDict,enemyListDict):
    #move towards largest cluster of enemies within a distance equal to attack range, attack each enemy, if you have attacks left, start
    #towards new cluster, if you have movement left, move to relative safety, if not paired with an emp
    for ship in myListDict['Juggernaut']:
#      ship.move(ship.getX()-ship.getMaxMovement()/2,ship.getY()-ship.getMaxMovement()/2)
      attacksLeft = ship.getAttacksLeft()
      
  def mineLayerControl(self,myListDict,enemyListDict):
  #create mine field around warp gate, if x amount of mines already near warp gate and have mines left, move towards
  #largest cluster dropping mines 
    for ship in myListDict['Mine Layer']:
      nearest = self.findNearest(ship,enemyShips)
#      nearest = self.findNearest(ship,enemyShips)
      self.smartMoveTo(ship,nearest,enemyListDict)
      if ship.getAttacksLeft()>0:
        ship.attack(ship)
              
  def supportControl(self,myListDict,enemyListDict):
    #if warpgate is below x health, move towards and heal warp Gate, else if wp in game,  move a support to them,  else move with largest cluster of friendly units
    target = myListDict['Warp Gate'][0]
    if target.getHealth() <= 2*target.getMaxHealth()/3:
      for ship in myListDict['Support']:
        self.smartMoveTo(ship,target,enemyListDict)
    else:
     for ship in myListDict['Support']:  
        target2 = self.findCluster(ship,ship.getOwner())
        if isinstance(target2,Ship) and target2.getType() != 'Mine' and target2.getType()!='Support':
          target = target2
        self.smartMoveTo(ship,target,enemyListDict)
           
  def empControl(self,myListDict,enemyListDict):
    #move towards largest cluster of enemy units, stun them. Works well with multi attackers
    print "emp",enemyListDict['Warp Gate']
    if len(enemyListDict['Warp Gate'])>0:
      target = enemyListDict['Warp Gate'][0]
    for ship in myListDict['EMP']:
      target2 = self.findCluster(ship,ship.getOwner()^1)
      if isinstance(target2,Ship):
        target = target2
      self.smartMoveTo(ship,target,enemyListDict)
      if len(self.allInRange(ship,ship.getRange(),ship.getOwner()^1))>2:
      #foe = self.bestUseAttack(ship,enemyShips)
      #if isinstance(foe,Ship) and ship.getAttacksLeft()>0:
        ship.attack(ship)
                       
  def stealthControl(self,myListDict,enemyListDict):
  #stick with other stealth ships, move towards most isolated enemy, or target emps or other priority targets, swarm them, then flee
    for ship in myListDict['Stealth']:
      nearest = self.findNearest(ship,enemyShips)
      self.smartMoveTo(ship,nearest,enemyListDict)
      self.smartAttack(ship,enemyListDict,self.ships)
	  #target = self.bestUseAttack(ship,enemyShips)
      #if isinstance(target,Ship):
      #  ship.attack(target)
      #  if target.getHealth()<1:
      #    enemyShips.remove(target)
      
         
  def cruiserControl(self,myListDict,enemyListDict):
    #mini battleship/big bomber
    for ship in myListDict['Cruiser']:
      nearest = self.findNearest(ship,enemyShips)
      self.smartMoveTo(ship,nearest,enemyListDict)
      self.smartAttack(ship,enemyListDict,self.ships)
#	  target = self.bestUseAttack(ship,enemyShips)
#     if isinstance(target,Ship) > 0:
#        ship.attack(target)
#        if target.getHealth() <1:
#         enemyShips.remove(target)
  
  def weapPlatControl(self,myListDict,enemyListDict):
    #stay far from enemy units, snipe priority targets (emp,stealth, etc)
    #TODO make attacking more efficient
    for ship in myListDict['Weapons Platform']:
      self.smartAttack(ship,enemyListDict,self.ships)
      #TODO make it so they attack anything that is shooting them
      nearest = self.findNearest(ship,enemyShips)
      self.moveAway(ship,nearest,enemyListDict['Mine'])

  def intercepControl(self,myListDict,enemyListDict):
  #mini juggernauts,
    pass
 #   for ship in myListDict['Interceptor']:
 #     ship.move(ship.getX()-2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
           
  def bomberControl(self,myListDict,enemyListDict):
    #attack stuff 
    for ship in myListDict['Bomber']:
      nearest = self.findNearest(ship,enemyShips)
      self.smartMoveTo(ship,nearest,enemyListDict)
      self.smartAttack(ship,enemyListDict,self.ships)
#	  target = self.bestUseAttack(ship,enemyShips)
#      if isinstance(target,Ship):
#        ship.attack(target)
#        if target.getHealth()<1:
#         enemyShips.remove(target)
             
  def mineControl(self,myListDict,enemyListDict):
    for ship in myListDict['Mine']:
#      print "HEY THERE I'M A MINE"
      targets = self.allInRange(ship,ship.getRadius(),enemyShips)
      if len(targets)>1:
        ship.selfDestruct()
             
  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  #takes a source (ship) and an owner. Finds all ships on the side given in range, returns a list of the ships    
  def allInRange(self, source, range,side):
    result = []
    for ship in self.ships:
#      if ship.getType()!= 'Mine':
        if ship.getOwner() == side and self.inRange(source.getX(), source.getY(), range, ship.getX(), ship.getY(), ship.getRadius()):
          result.append(ship)
    return result
  
  #takes a seeker (Ship that's trying to find group, a side (whose ships you're looking to find a group of) and a list of ships to look through
  #returns the ship that has the ships in your effective range
  def findCluster(self,seeker,side):
    groupSize = 0
    for ship in self.ships:
      currentSize = len(self.allInRange(ship,seeker.getRange(),side))
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
                
  def testWarp(self,warpShip):
     typeDict = {}
     type = 'Weapons Platform'
     for type in self.shipTypes:
       typeDict[type.getType()] = type
     energy = myPlayer[0].getEnergy()
     if type in typeDict:
       while energy >= typeDict[type].getCost():
         typeDict[type].warpIn(warpShip.getX(),warpShip.getY())                      
         energy-=typeDict[type].getCost()
            
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
  #goes through all enemies in range, and returns the a list of the enemy whose current health is closest to, but less than, that
  # ship's damage. If no such enemy fits this (i.e., no enemey has less health than damage), returns a list of the enemy with lowest health
#  def bestUseAttack(self,ship,ships):
#    foe = ship.getOwner()^1
#    targets = self.allInRange(ship,ship.getRange(),ships)
#    print "best use attack ships are ",ships
#    guy = 1
#    if len(targets) > 0:
#      health = 0
#      damage = ship.getDamage()
#      for target in targets:
#        if target.getHealth() > health and target.getHealth() <= damage:# and target.getMaxHealth() > maxHealth:
#          guy = target
#          health = target.getHealth()
#    return guy
   


  def bestUseAttack(self,ship,targets):
    foe = ship.getOwner()^1
    guy = 1
    health = 0
    damage = ship.getDamage()
    for target in targets:
      if target.getHealth() > health and target.getHealth() <= damage:# and target.getMaxHealth() > maxHealth:
        guy = target
        health = target.getHealth()
    return guy
    
    
  def priorityAttack(self,ship,enemyListDict,targets):
    attacksLeft = ship.getAttacksLeft()
    for type in typePriority:
      if type in enemyListDict:
        for foe in enemyListDict[type]:
          if foe in self.ships and foe in targets:
            return foe  
      
  def smartAttack(self,ship,enemyListDict,attackables):
    side = ship.getOwner()^1
    targets = self.allInRange(ship,ship.getRange(),side)
    if len(targets)>0:
      target = self.bestUseAttack(ship,targets)
      if isinstance(target,Ship) and target in self.ships:
        ship.attack(target)
      elif isinstance(target,int):
        target = self.priorityAttack(ship,enemyListDict,targets)                                        
        if isinstance(target,Ship):
          ship.attack(target)
          if target.getHealth()<1:  
            enemyListDict[target.getType()].remove(target)   
      return target
      
  def seppuku(self,ship):
    if ship.getHealth() <= ship.getMaxHealth()/5 or ship.getMaxAttacks() == 0:
      target = self.findNearest(ship,enemyShips)
      self.moveTo(ship,target)
      if self.inRange(ship.getX(),ship.getY(),ship.getRadius(),target.getX(),target.getY(),target.getRadius()):
        ship.selfDestruct()
    return 
  
  #TODO Specify quadrant
  def findPoints(self,centerX,centerY,radius,n):
    radius = int(95*radius/100)
    pi = 3.1415926535897932384626433832795028841971693993751058209
    Xval = [(int(math.floor((centerX + math.cos(2*pi/n*x)*radius)))) for x in range(0,n+1)]
    Yval = [(int(math.floor((centerY + math.sin(2*pi/n*y)*radius)))) for y in range(0,n+1)]
    return Xval,Yval
  
  def closingPoints(self,ship,target,radius,n):
    pi = 3.1415926535897932384626433832795028841971693993751058209
    modX = 1
    modY = 1
    if ship.getX()>target.getX():
      modX = -1
    if ship.getY()>target.getX():
      modY = -1
    Xval = [ship.getX() + math.cos((modX*pi/2)/n*x)*radius for x in range(0,n+1)]
    Yval = [ship.getY() + math.sin((modY*pi/2)/n*y)*radius for y in range(0,n+1)]
    return Xval,Yval
                                  
  def checkMove(self,x,y,radius,myShip,mines):
    if self.distance(0,x,0,y)+radius > self.mapRadius:
      return False
    else:
      for mine in mines:
        if self.inRange(x,y,radius,mine.getX(),mine.getY(),mine.getRange()):
          return False
      for ship in self.ships:
        if ship.getOwner()!=myShip.getOwner() and self.inRange(x,y,radius,ship.getX(),ship.getY(),ship.getRadius()):
          return False
    return True
  
  def moveInRange(self,ship,target,movement,mines):
    Xpoints,Ypoints = self.closingPoints(ship,target,movement,closingPoints)
    distance = 1005;x=-9999;y=-9999
    for i in range(len(Xpoints)):
      newDis = self.distance(Xpoints[i],target.getX(),Ypoints[i],target.getY())            
      if newDis < distance:
        for mine in mines:
          if self.inRange(Xpoints[i],Ypoints[i],ship.getRadius(),mine.getY(),mine.getX(),mine.getRadius()):
            if self.canEscape(Xpoints[i],Ypoints[i],ship.getRadius(),mine,ship.getMovementLeft()-movement):
              x = Xpoints[i]
              y = Ypoints[i]
          else:
            x = Xpoints[i]
            y = Ypoints[i]
    if x!=-9999 and y != -9999:
      print "x is ",x," y is ",y
      ship.move(int(x),int(y))             

  def moveTo(self,ship,target,mines):
    Xpoints,Ypoints = self.findPoints(ship.getX(),ship.getY(),ship.getMovementLeft(),numPoints)
    distance = 1005; x=-9999;y=-9999
    for i in range(len(Xpoints)):
      newDis = self.distance(Xpoints[i],target.getX(),Ypoints[i],target.getY())
      if newDis < distance and self.checkMove(Xpoints[i],Ypoints[i],ship.getRadius(),ship,mines):
        distance = newDis
        x = Xpoints[i]
        y = Ypoints[i]
    if x!=-9999 and y!=-9999:
      ship.move(x,y)
       
  def moveAway(self,ship,target,mines):
    Xpoints,Ypoints = self.findPoints(ship.getX(),ship.getY(),ship.getMovementLeft(),numPoints)
    distance = 0; x = -9999;y=-9999
    for i in range(len(Xpoints)):
      newDis = self.distance(Xpoints[i],target.getX(),Ypoints[i],target.getY())
      if newDis > distance and self.checkMove(Xpoints[i],Ypoints[i],ship.getRadius(),ship,mines):
        distance = newDis
        x = Xpoints[i]
        y = Ypoints[i]
    if x!=-9999 and y!=-9999:
      ship.move(x,y)
                                                      
  def smartMoveTo(self,ship,target,enemyListDict):
    disAway = self.distance(target.getX(),ship.getX(),target.getY(),ship.getY())-(ship.getRange()+target.getRadius())
#    print "disaway is ",self.distance(target.getX(),ship.getX(),target.getY(),ship.getY()), ship.getRange()+target.getRadius(),disAway," "
#    if disAway<=ship.getMovementLeft():
#      self.moveInRange(ship,target,disAway,enemyListDict['Mine'])              
#    else:
    self.moveTo(ship,target,enemyListDict['Mine'])
  
  def moveAwayTo(self,ship,target,myListDict):
    pass
  
  def canEscape(self,x,y,radius,target,move):
    print "can I escape"
    if self.distance(x,target.getX(),y,target.getY())-(radius+target.getRange()) >= move:
      return False
    else:
      return True
      
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
      types+=['Mine']
    
    for ship in self.ships:
      if ship.getOwner() == foePlayer[0].getId():
        enemyShips.append(ship)
      if ship.getOwner() == myPlayer[0].getId():
        myShips.append(ship)
    
    #dictionary magic
#    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mineLays,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber,'Mine':self.mines}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interceps,'Bomber':bombers,'Mine':mines}
    enemyListDict = {'Warp Gate':foewarps,'Battleship':foebatShips,'Juggernaut':foejuggs,'Mine Layer':foemineLayers,'Support':foesupports,'EMP':foeemps,'Stealth':foestealths,'Cruiser':foecruisers,'Weapons Platform':foeweapPlats,'Interceptor':foeinterceps,'Bomber':foebombers,'Mine':foemines}
    controlDict = {'Warp Gate':self.warpControl,'Battleship':self.batShipControl,'Juggernaut':self.juggControl,'Mine Layer':self.mineLayerControl,'Support':self.supportControl,'EMP':self.empControl,'Stealth':self.stealthControl,'Cruiser':self.cruiserControl,'Weapons Platform':self.weapPlatControl,'Interceptor':self.intercepControl,'Bomber':self.bomberControl,'Mine':self.mineControl}
	
    for ty in types:
      try:
        #myListDict[ty] = funDict[ty](myPlayer[0].getId(),self.ships)  
        myListDict[ty] = self.typeList(self.playerID,self.ships,ty)
        enemyListDict[ty] = self.typeList(self.playerID^1,self.ships,ty)
        #enemyListDict[ty] = funDict[ty](foePlayer[0].getId(),self.ships)
      except KeyError:
        pass #print ty
   
    for ty in myListDict:
       try:
         controlDict[ty](myListDict,enemyListDict)
       except KeyError:
         pass #print ty
    
    #end dictionary magic
    
#    for ship in myShips:
#      self.seppuku(ship)
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
