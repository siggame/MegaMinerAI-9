#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math

class Vect(object):
  def __init__(self, x, y):
    self.x = int(x)
    self.y = int(y)

  def getX(self): return self.x
  def getY(self): return self.y

  @property
  def magnitude(self):
    return int(math.ceil(math.sqrt(self.x ** 2 + self.y ** 2)))
  
  @staticmethod
  def vectorize(ship, target):
    return Vect(ship.getX() - target.getX(), ship.getY() - target.getY())

  @staticmethod
  def randVect(maxMag):
    angle = random.uniform(0, math.pi * 2)
    mag = random.uniform(0, maxMag)
    v = Vect(mag*math.cos(angle), mag*math.sin(angle))
    if not (0 <= v.magnitude <= maxMag):
      raise Exception("Random vector too long")
    return v
 
  def makeUnit(self):
    ret = Vect(self.x, self.y)
    startMag = self.magnitude
    if 0 != startMag != 1:
      ret.x/=startMag
      ret.y/=startMag
    if 0 != ret.magnitude != 1:
      raise Exception("Make Unit Fail")
    return ret
  
  def scale(self, scalar):
    ret = Vect(self.x, self.y)
    ret.x *= scalar
    ret.y *= scalar
    return ret
  
  def diff(self, other):
    return Vect(other.x - self.x, other.y - self.y)
  
  def startFrom(self, ship):
    return (ship.getX() + self.x, ship.getY() + self.y)
  
  def startFromV(self, ship):
    return Vect(*self.startFrom(ship))
  
  def moveShip(self, ship):
    ship.move(*self.startFrom(ship))
  
  def __repr__(self):
    return "(%i, %i, %i)"%(self.x, self.y, self.magnitude)

  def __str__(self):
    return repr(self)

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  def validPos(self, ship, pos):
    if not (self.innerMapRadius() + ship.getRadius() <= pos.magnitude <= self.outerMapRadius() - ship.getRadius()):
      #print pos, self.innerMapRadius(), pos.magnitude, self.outerMapRadius()
      return False
    return True

  def validMove(self, ship, vect):
    pos = vect.startFromV(ship)
    return self.validPos(ship, pos)

  def spreadMove(self, ship, target):
    possible = [Vect.randVect(ship.getMovementLeft()).startFromV(ship) for _ in range(1000)]
    possible = filter(lambda pos: self.validPos(ship, pos), possible)
    #possible.append(Vect(ship.getX(), ship.getY()))
    move = min(possible, key=lambda pos: Vect.vectorize(target, pos).magnitude)
    print move
    if move.x != ship.getX() or move.y != ship.getY():
            
      ship.move(move.x, move.y)

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    for ship in self.ships:
      if ship.getOwner() == self.playerID():
        for target in self.ships:
          if target.getOwner() != self.playerID():
            self.spreadMove(ship, target)
            #move = Vect.vectorize(ship, target)
            #print move, move.makeUnit(), move.makeUnit().scale(ship.getMovementLeft())
            #move = move.makeUnit().scale(ship.getMovementLeft())
            #if self.validMove(ship, move):
            #  move.moveShip(ship)
            break
    return True

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
