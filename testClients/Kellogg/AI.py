#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

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
         
  def end(self):
    pass

  def distance(self,fromX, toX, fromY, toY):
    return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))
    
  def inRange(self,x1, y1, rad1, x2, y2, rad2):
    return self.distance(x1, x2, y1, y2) <= rad1 + rad2
      
  def allInRange(self, source):
    result = []
    range = source.getRange(); owner = source.getOwner()
    if source.getType() != 'Support':
      for ship in self.ships:
          if ship.getOwner() != owner and self.inRange(source.getX(), source.getY(), range, ship.getX(), ship.getY(), ship.getRadius()):
            result.append(ship)
    elif source.getType() == 'Support':
      for ship in self.ships:
        if ship.getOwner() == owner and self.inRange(source.getX(), source.getY(), range, ship.getX(), ship.getY(), ship.getRadius()):
         result.append(ship)
    else:
      print source.getType(), "from allInRange, unrecognized type"                       
    return result
  
  
  
  def moveToTarget(self,ship,target):
    maxMove = ship.getMaxMovement()
    dx = -(ship.getX()-target.getX())
    dy = -(ship.getY()-target.getY())
    dist = abs(dx)+abs(dy)
    if dist > maxMove:
      dx = dx/10
      dy = dy/10
    ship.move(ship.getX()+dx,ship.getY()+dy)
    maxMove-=dist
                                             
  
  
  def smartWarp(self,warpShip,type,shipsOfType):
     #TODO: make smart
     print "WARPING IN A ",type.getType()
     type.warpIn(warpShip.getX(),warpShip.getY())
 
  def bestUseAttack(self,ship):
    print "HERE IS THE SHIP TRYING TO ATTACK", ship.getType()
    targets = self.allInRange(ship)
    health = 0
    minHealth = 10000
    damage = ship.getDamage()
    maxAttacks = ship.getMaxAttacks()
    if len(targets)>0:
      while maxAttacks > 0:
        for target in targets:
          if target.getHealth() > health and target.getHealth() <= damage:# and target.getMaxHealth() > maxHealth:
            guy = target
            health = target.getHealth()
          elif target.getHealth() < minHealth:
            guy = target
            minHealth = target.getHealth()        
        ship.attack(guy)
        if guy in targets:
          targets.remove(guy)
        maxAttacks-=1
 
  def run(self):
    #Gah, so many ships
    types = []
    warps = []
    batShips = []
    juggs = []
    mineLayers = []
    supports = []
    emps = []
    stealths = []
    cruisers = []
    weapPlats = []
    interCeps = []
    bombers = []
    enemy = []
    myShips = []
       
    shipTypes = self.shipTypes
    #get string of each ship type
    for type in shipTypes:
      types.append(type.getType())
      
    ships = self.ships
    for pl in self.players:
      if self.playerID() == pl.getId():
        myPlayer = pl
      else:
        foePlayer = pl
    types = types + ['Warp Gate']

    
    for ship in self.ships:
      if ship.getType() == 'Warp Gate' and ship.getOwner() == foePlayer.getId():
        enemy.append(ship)
        foeWarp = ship
      elif ship.getOwner == foePlayer.getId():
        enemy.apend(ship)
    
    funDict = {'Warp Gate':self.warp,'Battleship':self.battleship,'Juggernaut':self.juggernaut,'Mine Layer':self.mines,'Support':self.support,'EMP':self.emp,'Stealth':self.stealth,'Cruiser':self.cruiser,'Weapons Platform':self.weapons,'Interceptor':self.interceptor,'Bomber':self.bomber}
    myListDict = {'Warp Gate':warps,'Battleship':batShips,'Juggernaut':juggs,'Mine Layer':mineLayers,'Support':supports,'EMP':emps,'Stealth':stealths,'Cruiser':cruisers,'Weapons Platform':weapPlats,'Interceptor':interCeps,'Bomber':bombers}
    
    
    for ty in types:
      try:
        myListDict[ty] = funDict[ty](myPlayer.getId(),ships)  
      except KeyError:
        print "something bad happened making myListDict",ty
   # print "HERE'S THE LIST OF ALL MY SHIPS, SPLIT BY TYPE",myListDict
    
    for w in myListDict['Warp Gate']:
      w.move(w.getX()+10,w.getY()+10)
      for type in shipTypes:
        if type.getCost() <= myPlayer.getEnergy():
          self.smartWarp(w,type,myListDict[type.getType()])
    for ty in types:
      for ship in myListDict[ty]:
        self.moveToTarget(ship,foeWarp)
        self.bestUseAttack(ship)
        
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
