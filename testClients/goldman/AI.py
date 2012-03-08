#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math
def distance(fromX, fromY, toX, toY):
  return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))

def inRange(x1, y1, rad1, x2, y2, rad2):
  return distance(x1, y1, x2, y2) <= rad1 + rad2
  
def travelDist(x1, y1, rad1, x2, y2, rad2):
  return distance(x1, y1, x2, y2) - (rad1 + rad2)

def getMeThere(x1, y1, rad1, x2, y2, rad2, movementLeft, retreat=False, reverse=False):
  move = distance(x1, y1, x2, y2) - (rad1 + rad2)
  heading = 1
  if reverse:
    heading = -1
  
  if move < 0 and not retreat:
    return [x1, y1]
  if abs(move) > movementLeft:
    move = movementLeft if move > 0 else -movementLeft

  dx, dy = x2-x1, y2-y1
  if dx != 0:
    angle = math.atan(dy / float(dx))
    x = move * math.cos(angle) * cmp(dx, 0) * heading + x1
    y = move * math.sin(angle) * cmp(dy, 0) * heading + y1
  else:
    x = x1
    y = move * cmp(dy, 0) * heading + y1  
  return map(int, (x, y))
  
def safeMove(ship, move):
  if (ship.getX(), ship.getY()) != tuple(move) and distance(move[0], move[1], 0, 0) < 500:
    ship.move(*move)


class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "goldman"

  @staticmethod
  def password():
    return "ROBOTHOUSE"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass


  def spendEnergy(self):
    cheapEnough = lambda shipType: shipType.getCost() <= self.players[self.playerID()].getEnergy()
    for shipType in filter(cheapEnough, self.shipTypes):
      if shipType.getType() == "Mine Layer":
        shipType.warpIn(self.myGate.getX(), self.myGate.getY())
        shipType.warpIn(self.myGate.getX(), self.myGate.getY())
        shipType.warpIn(self.myGate.getX(), self.myGate.getY())
      if shipType.getType() == "Weapons Platform":
        shipType.warpIn(self.myGate.getX(), self.myGate.getY())
    while True:
      canBuy = filter(cheapEnough, self.shipTypes)
      try:
        spammers = filter(lambda shipType: shipType.getType() in ["BattleShip", "Juggernaught", "Bomber", "Interceptor"], canBuy)
        if len(spammers) > 0:
          canBuy = spammers
        
        random.choice(canBuy).warpIn(self.myGate.getX(), self.myGate.getY())
      except IndexError:
        break
  def setup(self):
    self.myShips = filter(lambda ship: ship.getOwner() == self.playerID(), self.ships)
    self.theirShips = filter(lambda ship: ship.getOwner() != self.playerID(), self.ships)
    self.myGate = filter(lambda ship: ship.getType() == "Warp Gate", self.myShips)[0]
    self.theirGate = filter(lambda ship: ship.getType() == "Warp Gate", self.theirShips)[0]
    
  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.setup()
    self.spendEnergy()
    mines = filter(lambda target: target.getType() == "Mine" and target.getOwner() != self.playerID(), self.theirShips)
    for ship in self.myShips:
      attackable = filter(lambda target: target.getHealth() > 0 and target.getType() != "Mine", self.theirShips)
      if ship.getMaxAttacks() == 0 and ship.getSelfDestructDamage() != 0:
        ship.selfDestruct()
      while ship.getAttacksLeft() > 0 and len(attackable) > 0:
        if ship.getType() == "Mine Layer":
          target = min(attackable, key=lambda target: (target.getDamage() == 0, 
                                                       travelDist(ship.getX(), ship.getY(), ship.getRange(), target.getX(), target.getY(), target.getRadius())))
          move = getMeThere(ship.getX(), ship.getY(), 0, target.getX(), target.getY(), 0, ship.getMovementLeft())
          safeMove(ship, move)
          if inRange(ship.getX(), ship.getY(), 45, target.getX(), target.getY(), target.getRadius()):
            ship.attack(ship)
            attackable.remove(target)
          break
        else:
          target = min(attackable, key=lambda target: (target.getType() != "Weapons Platform", 
                                                       travelDist(ship.getX(), ship.getY(), ship.getRange(), target.getX(), target.getY(), target.getRadius())))
          move = getMeThere(ship.getX(), ship.getY(), ship.getRange(), target.getX(), target.getY(), target.getRadius(), ship.getMovementLeft())
          safeMove(ship, move)
          if inRange(ship.getX(), ship.getY(), ship.getRange(), target.getX(), target.getY(), target.getRadius()):
            ship.attack(target)
            attackable.remove(target)
          else:
            break
      #if ship.getMovementLeft() > 0:
      #  direction = random.choice([(0, 1), (1, 0), (-1, 0), (0, -1)])
      #  move = ship.getMovementLeft()*direction
      #  move = move[0] + ship.getX(), move[1] + ship.getY()
      #  print "WOO", direction, ship.getMovementLeft(), ship.getType()
      #  safeMove(ship, move)
      #if ship.getMovementLeft() > 0:
      #  move = getMeThere(ship.getX(), ship.getY(), 0, self.theirGate.getX(), self.theirGate.getY(), 0, ship.getMovementLeft(), reverse=True)
      #  safeMove(ship, move)
    return 1

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
