#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

enemyShips = []
myPlayer = []
foePlayer = []
foeWarp = []

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
         
  def warpControl(self,warps,enemy,myListDict):
    print "warp control"
    for w in myListDict['Warp Gate']:
      w.move(w.getX()+10,w.getY()-10)
      self.smartWarp(w)
  
  def batShipControl(self,batShips,enemy,myListDict):
    #Move towards enemy warp gate. if not in range of warp gate, attack enemy with most health that you can kill
    #once in range of warp gate, attack. if health is below x%, fire and self destruct
    for ship in batShips:
      ship.move(ship.getX()+ship.getMaxMovement()/2,ship.getY()+ship.getMaxMovement()/2)
  
  def juggControl(self,juggs,enemys,myListDict):
    #move towards largest cluster of enemies within a distance equal to attack range, attack each enemy, if you have attacks left, start
    #towards new cluster, if you have movement left, move to relative safety, if not paired with an emp
    for ship in juggs:
      ship.move(ship.getX()-ship.getMaxMovement()/2,ship.getY()-ship.getMaxMovement()/2)

  def mineLayerControl(self,mineLayers,enemy,myListDict):
  #create mine field around warp gate, if x amount of mines already near warp gate and have mines left, move towards
  #largest cluster dropping mines 
    for ship in mineLayers:
      ship.move(ship.getX()-ship.getMaxMovement()/5,ship.getY()+ship.getMaxMovement()/2)
      ship.attack(ship)
              
  def supportControl(self,supports,enemy,myListDict):
    #if warpgate is below x health, move towards and heal warp Gate, else move with largest cluster of friendly units
    for ship in supports:
      ship.move(ship.getX()+ship.getMaxMovement()/2,ship.getY()-ship.getMaxMovement()/2)
           
  def empControl(self,emps,enemy,myListDict):
    #move towards largest cluster of enemy units, stun them. Works well with mulit attackers
    for ship in emps:
      print foeWarp[0],ship
      self.moveToTarget(ship,foeWarp[0])
      foe = self.bestUseAttack(ship)
      if len(foe) > 0:
        ship.attack(ship)
                       
  def stealthControl(self,stealths,enemy,myListDict):
  #stick with other stealth ships, move towards most isolated enemy, or target emps or other priority targets, swarm them, then flee
    for ship in stealths:
      ship.move(ship.getX()+ship.getMaxMovement(),ship.getY())
         
  def cruiserControl(self,cruisers,enemy,myListDict):
    #not sure yet
    for ship in cruisers:
      ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()+2*ship.getMaxMovement()/3)
  
  def weapPlatControl(self,weapPlats,enemy,myListDict):
    #stay far from enemy units, snipe priority targets (emp,stealth, etc)
    for ship in weapPlats:
      ship.move(ship.getX()+2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
  
  def intercepControl(self,interceps,enemy,myListDict):
  #not sure yet
    for ship in interceps:
      ship.move(ship.getX()-2*ship.getMaxMovement()/3,ship.getY()+ship.getMaxMovement()/3)
           
  def bomberControl(self,bombers,enemy,myListDict):
    #attack stuff
    for ship in bombers:
      ship.move(ship.getX()+ship.getMaxMovement()/3,ship.getY()-2*ship.getMaxMovement()/3)
             
  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  def allInRange(self, source, side):
    result = []
    range = source.getRange()
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
      dx = int(math.copysign(maxMove/5,dx))
      dy = int(math.copysign(maxMove/5,dy))
    if abs(dx)+abs(dy)>0:
      ship.move(ship.getX()+dx,ship.getY()+dy)
    maxMove-=dist
       
  def findCluster(self,ship):
    pass
#    cluster = 0
#    clusterList = []
#    for enemy in enemyShips:       
#    pass
  
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
     print "calling warp"
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
     print "types,mincost,energy",types,minCost,energy
     while energy >= minCost:
       if 'Battleship' in types:
         for type in shipTypes:
           if type.getType() == 'BattleShip' and energy >= type.getCost():
             type.warpIn(warpShip.getX()+10,warpShip.getY())
             energy-=type.getCost()
       elif 'Juggernaut' in types:
         for type in shipTypes:
           if type.getType() == 'Juggernaut' and energy >= type.getCost():
             type.warpIn(warpShip.getX()-10,warpShip.getY())
             energy-=type.getCost()
       if 'Mine Layer' in types:
         for type in shipTypes:
           if type.getType() == 'Mine Layer' and energy >= type.getCost():
             type.warpIn(warpShip.getX(),warpShip.getY()+10)
             energy-=type.getCost()
       if 'Support' in types:
         for type in shipTypes:
           if type.getType() == 'Support' and energy >= type.getCost():
             type.warpIn(warpShip.getX(),warpShip.getY()+10)
             energy-=type.getCost()
       if 'EMP' in types:
          for type in shipTypes:
            if type.getType() == 'EMP' and energy >= type.getCost():
              type.warpIn(warpShip.getX(),warpShip.getY()+10)                                                          
              energy-=type.getCost()
       if 'Stealth' in types:
         for type in shipTypes:
           if type.getType() == 'Stealth' and energy >= type.getCost():
             type.warpIn(warpShip.getX(),warpShip.getY()+10)
             energy-=type.getCost()
       if 'Cruiser' in types:
          for type in shipTypes:
            if type.getType() == 'Cruiser' and energy >= type.getCost():
              type.warpIn(warpShip.getX(),warpShip.getY()+10)
              energy-=type.getCost()
       if 'Weapons Platforms' in types:
          for type in shipTypes:
            if type.getType() == 'Weapons Platform' and energy >= type.getCost():
              type.warpIn(warpShip.getX(),warpShip.getY()+10)
              energy-=type.getCost()
       if 'Interceptor' in types:
         for type in shipTypes:
           if type.getType() == 'Interceptor' and energy >= type.getCost():
             type.warpIn(warpShip.getX(),warpShip.getY()+10)
             energy-=type.getCost()
       if 'Bomber' in types:
         for type in shipTypes:
           if type.getType() == 'Bomber' and energy >= type.getCost():
            type.warpIn(warpShip.getX(),warpShip.getY()+10)
            energy-=type.getCost()
     return
                                                                                                                                                                                                                                                                                     
  #goes through all enemies in range, and returns the a list of the enemy whose current health is closest to, but less than, that ships damage. 
  #If no such enemy fits this (i.e., no enemey has less health than damage), returns a list of the enemy with lowest health
  def bestUseAttack(self,ship):
    foe = ship.getOwner()^1
    targets = self.allInRange(ship,foe)
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
    
  def dumbAttack(self,ship):
      attacks = ship.getMaxAttacks()
      targets = self.allInRange(ship)
      for target in targets: 
        if attacks > 0:
          ship.attack(target)
          attacks-=1
        
  def run(self):
    #Gah, so many ships
    types=[]; warps=[]; batShips=[]; juggs=[]; mineLayers=[]; supports=[]; myships=[]
    emps=[]; stealths=[]; cruisers=[]; weapPlats=[]; interceps=[]; bombers=[]; enemy=[]
       
    del foeWarp[0:len(foeWarp)]
    del enemyShips[0:len(enemyShips)]
    
    
    shipTypes = self.shipTypes
    #get string of each ship type
    for type in shipTypes:
      types.append(type.getType())
    types+=['Warp Gate']  

    #find out who I am, and my foe
#    for pl in self.players:
#      if self.playerID() == pl.getId():
#        myPlayer.append(pl)
#      else:
#        foePlayer.append(pl)
    
    #find enemy warp gate and make list of enemy ships
    
    ships = self.ships
    
    for ship in self.ships:
      if ship.getType() == 'Warp Gate' and ship.getOwner() == foePlayer[0].getId():
        enemy.append(ship)
        foeWarp.append(ship)
      elif ship.getOwner == foePlayer[0].getId():
        enemyShips.apend(ship)
    
    #dictionary magic
    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mines,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interceps,'Bomber':bombers}
    controlDict = {'Warp Gate':self.warpControl,'Battleship':self.batShipControl,'Juggernaut':self.juggControl,'Mine Layer':self.mineLayerControl,'Support':self.supportControl,'EMP':self.empControl,'Stealth':self.stealthControl,'Cruiser':self.cruiserControl,'Weapons Platform':self.weapPlatControl,'Interceptor':self.intercepControl,'Bomber':self.bomberControl}
    
    for ty in types:
      try:
        myListDict[ty] = funDict[ty](myPlayer[0].getId(),ships)  
      except KeyError:
        pass
   
    for ty in myListDict:
       controlDict[ty](myListDict[ty],enemy,myListDict)
       
    #for ty in types:
    #  for ship in myListDict[ty]:
    #    self.moveToTarget(ship,foeWarp[0])
    #    attackList = self.bestUseAttack(ship)
    #    if len(attackList) > 0 and ship.getAttacksLeft() > 0:
    #      ship.attack(attackList[0])
    #    if ship.getType()!= 'Warp Gate':
    #      if self.turnNumber()%100>90 or ship.getHealth()<ship.getMaxHealth()/4:
    #        ship.selfDestruct()
#OLD CODE    
    #myships = []
    #enemy = []
    #randShip = random.randrange(0,4)
    #newshiptype = self.shipTypes[randShip]
 
    #distinguish my ships from enemy ships
    #for ship in self.ships:
    #   if ship.getOwner() == self.playerID():
    #     myships.append(ship)
    #   elif ship.getOwner() != self.playerID():
    #     enemy.append(ship)
    
    #for ship in myships:
    #   move = ship.getMaxMovement()
    #   attack = ship.getMaxAttacks()
    #   #warp in ships
    #   if ship.getType() == "Warp Gate": 
    #     newshiptype.warpIn(ship.getX(),ship.getY())
    #   #attacky stuff
    #   for foe in enemy:
    #      if ship.getAttacksLeft()>0:
    #       if ship.getType() == "Mine Layer" and self.distance(ship.getX(),ship.getY(),foe.getX(),foe.getY())<=ship.getRange():
    #         ship.attack(ship)                   
    #       elif self.inRange(ship.getX(),ship.getY(), ship.getRadius(), foe.getX(), foe.getY(), foe.getRadius()):
    #         ship.attack(foe)
       #movey stuff
    #   dirX = 0; dirY = 0; randX = 0; randY = 0
    #   randX = random.randrange(-10,10)
    #   randY = random.randrange(-10,10)
    #   while move > 0:
    #     if ship.getX() > 0:
    #        dirX = -1*ship.getMovementLeft()/5
    #     elif ship.getX() < 0:
    #        dirX = ship.getMovementLeft()/5
    #     if ship.getY() > 10:
    #       dirY = -1*ship.getMovementLeft()/5
    #     elif ship.getY() < 10:
    #       dirY = ship.getMovementLeft()/5
    #     dis = self.distance(ship.getX(),ship.getY(),ship.getX()+dirX,ship.getY()+dirY)
    #     if dis <= ship.getMovementLeft() and  dis >0:
    #       ship.move(ship.getX()+dirX,ship.getY()+dirY)
    #     move -= dis
    #   if self.turnNumber()%100 >= 95:
    #     ship.selfDestruct()"""
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
