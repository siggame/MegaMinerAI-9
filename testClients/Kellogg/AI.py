#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

myShipsDict = {}

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Kellogg"

  @staticmethod
  def password():
    return "password"

  def init(self):
    pass 
    
  def warp(self,player,ships):
    warp = []
    for ship in ships:
      if ship.getOwner() == player and ship.getType() == "Warp Gate":
        warp.append(ship)
#    print "lenght of warp is ",len(warp)
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
         
  def warpControl(self,warps,enemy):
    print "Warp Control"
  
  def batShipControl(self,batShips,enemy):
    print "BatShip Control"
  
  def juggControl(self,jugg,enemys):
    print "JuggControl"

  def mineLayerControl(self,mineLayers,enemy):
    print "MineLayerControl"
    
  def supportControl(self,supports,enemy):
    print "Support Control"
    
  def empControl(self,emps,enemy):
    print "emp control"
    
  def stealthControl(self,stealths,enemy):
    print "Stealth Control"
  
  def cruiserControl(self,cruisers,enemy):
    print "Cruiser Control"
  
  def weapPlatControl(self,weapPlats,enemy):
    print "weapPlate Control"
  
  def intercepControl(self,interceps,enemy):
    print "intercepControl"
    
  def bomberControl(self,bombers,enemy):
    print "bomber Control"
      
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
      dx = int(math.copysign(maxMove/2,dx))
      dy = int(math.copysign(maxMove/2,dy))
    ship.move(ship.getX()+dx,ship.getY()+dy)
    maxMove-=dist
       
  def findCluster(self,ship):
    pass
  
  def findNearest(self,ship,ships):
    pass
                
  def moveInRange(self,ship,target):
    maxMove = ship.getMaxMovement()
#    while maxMove > 0 and not inRange(ship.getX(),ship.getY(),ship.getRange(),target.getX(),target.getY(),target.getRadius):
    pass
  
  def moveOutRange(self,ship,target):
    pass
  
  def smartWarp(self,warpShip,type):
     #TODO: make smart
#     print "WARPING IN A ",type.getType()
     type.warpIn(warpShip.getX(),warpShip.getY())
 
  #goes through all enemies in range, and returns the enemy whose current health is closest to, but less than, that ships damage. 
  #If no such enemy fits this (i.e., no enemey has less health than damage), returns enemy with lowest health
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
       
    shipTypes = self.shipTypes
    #get string of each ship type
    for type in shipTypes:
      types.append(type.getType())
      
    ships = self.ships
    #find out who I am
    for pl in self.players:
      if self.playerID() == pl.getId():
        myPlayer = pl
      else:
        foePlayer = pl
    types+=['Warp Gate']
    
    #find enemy warp gate and make list of enemy ships
    for ship in self.ships:
      if ship.getType() == 'Warp Gate' and ship.getOwner() == foePlayer.getId():
        enemy.append(ship)
        foeWarp = ship
      elif ship.getOwner == foePlayer.getId():
        enemy.apend(ship)
    
    #dictionary magic
    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mines,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interceps,'Bomber':bombers}
    controlDict = {'Warp Gate':self.warpControl,'Battleship':self.batShipControl,'Juggernaut':self.juggControl,'Mine Layer':self.mineLayerControl,'Support':self.supportControl,'EMP':self.empControl,'Stealth':self.stealthControl,'Cruiser':self.cruiserControl,'Weapons Platform':self.weapPlatControl,'Interceptor':self.intercepControl,'Bomber':self.bomberControl}
    
    for ty in types:
      try:
        myListDict[ty] = funDict[ty](myPlayer.getId(),ships)  
      except KeyError:
        pass
   
    for ty in myListDict:
       controlDict[ty](myListDict[ty],enemy)
       
    myShipsDict = myListDict
    energy = myPlayer.getEnergy()
    for w in myListDict['Warp Gate']:
      w.move(w.getX()+10,w.getY()-10)
      for type in shipTypes:
        if type.getCost() <= energy:
          self.smartWarp(w,type)
          energy -= type.getCost()
    for ty in types:
      for ship in myListDict[ty]:
        self.moveToTarget(ship,foeWarp)
        attackList = self.bestUseAttack(ship)
        if len(attackList) > 0 and ship.getAttacksLeft() > 0:
          ship.attack(attackList[0])
        if ship.getHealth() < ship.getMaxHealth()/4 and ship.getType() != 'Warp Gate' or self.turnNumber()%100 >85:
          ship.selfDestruct()
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
