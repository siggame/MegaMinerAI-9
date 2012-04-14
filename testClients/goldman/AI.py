#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import random
import math
import json

def addFunction(objType):
    def wrap(fun):
        setattr(objType, fun.__name__, fun)
    return wrap

def listof(fun, key, data):
  result = key(fun(data, key=key))
  return [datum for datum in data if key(datum) == result]

def saveConfiguration(data, filename="data.dat"):
    with open(filename, 'w') as f:
        json.dump(data, f)

def loadConfiguration(filename="data.dat"):
    try:
      with open(filename, 'r') as f:
          return json.load(f)
    except IOError:
      return {}

class Vect(object):
  def __init__(self, x, y):
    self.x = int(x)
    self.y = int(y)

  @property
  def magnitude(self):
    return int(math.ceil(math.sqrt(self.x ** 2 + self.y ** 2)))
  
  @staticmethod
  def vectorize(ship, target):
    return Vect(ship.x - target.x, ship.y - target.y)

  @staticmethod
  def randVect(maxMag):
    angle = random.uniform(0, math.pi * 2)
    #mag = math.sqrt(random.random()) * maxMag
    mag = maxMag * random.choice([1.0 / 4, 1.0 / 2, 1.0])
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
    return (ship.x + self.x, ship.y + self.y)
  
  def startFromV(self, ship):
    return Vect(*self.startFrom(ship))
  
  def moveShip(self, ship):
    ship.move(*self.startFrom(ship))
  
  def __repr__(self):
    return "(%i, %i, %i)"%(self.x, self.y, self.magnitude)

  def __str__(self):
    return repr(self)

  def __hash__(self):
    return repr(self).__hash__()

@addFunction(Ship)
def cloud(self, density=100):
  return [Vect.randVect(self.movementLeft).startFromV(self) for _ in range(density)] + [Vect(self.x, self.y)]

@addFunction(Ship)
def listReduce(self, fun, data):
  result = fun(data, self)
  if len(result) == 0:
    return data
  return result

@addFunction(Ship)
def canShoot(self, target, pos=None):
  if pos == None:
    pos = self
  if target.id not in self.targeted:
    if self.attacksLeft > 0:
      if Vect.vectorize(target, pos).magnitude <= self.range + target.radius:
        return True
  return False

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "goldman"

  @staticmethod
  def password():
    return "password"


  def nextRound(self):
    self.availableTypes = "_".join(sorted([shipType.type for shipType in self.shipTypes]))
    print 'AVAIL?', self.availableTypes
    stored = loadConfiguration()
    try:
      options = stored[self.availableTypes]
    except KeyError:
      stored[self.availableTypes] = {}
      options = stored[self.availableTypes]
    try:
      maxValue = max(options.itervalues())
    except ValueError:
      maxValue = -1
    if maxValue <= 0:
      # Create a new set of options
      energy = self.players[self.playerID].energy
      config = dict((shipType.type, 0) for shipType in self.shipTypes)
      while True:
        afford = filter(lambda shipType: shipType.cost <= energy, self.shipTypes)
        if len(afford) == 0:
          break
        choose = random.choice(afford)
        config[choose.type] += 1
        energy -= choose.cost
      self.spawned = tuple((value for key, value in sorted(config.items())))
      self.key = "_".join(map(str, self.spawned))
      options[self.key] = 1
    else:
      self.key = random.choice([key for key, value in options.iteritems() if value == maxValue])
      self.spawned = map(int, self.key.split("_"))
    print self.spawned, self.key
    for i, shipType in enumerate(sorted(self.shipTypes, key=lambda shipType: shipType.type)):
      for _ in range(self.spawned[i]):
        shipType.warpIn(self.myGate.x, self.myGate.y)
    saveConfiguration(stored)
    
  def checkRoundWin(self):
    score = (self.players[self.playerID].victories, self.players[self.playerID^1].victories)
    # if the score has changed since you last checked
    if score != self.score:
      change = (score[0] - self.score[0], score[1] - self.score[1])
      stored = loadConfiguration()
      if change == (1, 0):
        stored[self.availableTypes][self.key] += 1
      elif change == (0, 1):
        stored[self.availableTypes][self.key] /= 2
      elif change != (1, 1):
        print "HOW THE FUCK?:", score, self.score
      self.score = score
      saveConfiguration(stored)
      self.nextRound()
      
  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    for shipType in self.shipTypes:
      print shipType
    #self.checkRoundWin()
    
  def validPos(self, options, ship):
    return [pos for pos in options if (pos.magnitude <= self.mapRadius - ship.radius)]

  def noMines(self, options, ship):
    def test(pos):
      for mine in self.theirMines:
        # TODO Consider allowing healthy ships to move through mines
        # TODO Consider allowing fast ships to hop in and out
        if Vect.vectorize(pos, mine).magnitude <= ship.radius + mine.radius:
          return False
      return True
    return [pos for pos in options if test(pos)]
    
    
  def minSelfStack(self, options, ship):
    scores = {}
    for pos in options:
      scores[pos] = 0
      for block in self.myShips:
        if block.type != "Warp Gate" and block.id != ship.id:
          if Vect.vectorize(block, pos).magnitude <= block.radius + ship.radius:
            scores[pos] += 1
    minScore = min(scores.itervalues())
    return [pos for pos in options if scores[pos] == minScore]
  
  def noSelfStack(self, options, ship):
    def test(pos):
      for block in self.myShips:
        if block.type != "Warp Gate" and block.id != ship.id:
          if Vect.vectorize(block, ship).magnitude <= block.radius + ship.radius:
            return False
      return True
    return [pos for pos in options if test(pos)]
  
  def nearest(self, options, ship):
    if ship.attacksLeft == 0:
      return []
    scores = {}
    for pos in options:
      scores[pos] = self.mapRadius * 2
      for target in self.theirShips:
        if ship.canShoot(target, pos):
          return self.mostTargets(options, ship)
        if target.id not in self.theirShips:
          scores[pos] = min(scores[pos], Vect.vectorize(target, pos).magnitude)        
    minScore = min(scores.itervalues())
    return [pos for pos in options if scores[pos] == minScore]
  
  def clump(self, options, ship):
    scores = {}
    for pos in options:
      scores[pos] = self.mapRadius * 2
      for target in self.myShips:
        if target.id != ship.id and target.health < target.maxHealth:
          dist = Vect.vectorize(target, pos).magnitude
          if dist <= ship.range + target.radius:
            return self.mostClump(options, ship)
          scores[pos] = min(scores[pos], dist)
    minScore = min(scores.itervalues())
    return [pos for pos in options if scores[pos] == minScore]
  
  def mostClump(self, options, ship):
    scores = {}
    for pos in options:
      scores[pos] = 0
      for target in self.myShips:
        if target.id != ship.id and target.health < target.maxHealth:
          dist = Vect.vectorize(target, pos).magnitude
          if dist <= ship.range + target.radius:
            scores[pos] += float(target.maxHealth - target.health) / target.maxHealth
    maxScore = max(scores.itervalues())
    return [pos for pos in options if scores[pos] == maxScore]

  def mostTargets(self, options, ship):
    if ship.attacksLeft == 0:
      return []
    scores = {}
    for pos in options:
      scores[pos] = 0
      for target in self.theirShips:
        if ship.canShoot(target, pos):
          scores[pos] += 1
    maxScore = max(scores.itervalues())
    if maxScore > ship.attacksLeft:
      maxScore = ship.attacksLeft
    return [pos for pos in options if scores[pos] >= maxScore]
    
  def mostLethal(self, options, ship):
    if ship.attacksLeft == 0:
      return []
    scores = {}
    for pos in options:
      scores[pos] = 0
      for target in self.theirShips:
        if ship.canShoot(target) and target.health <= ship.damage:
          scores[pos] += 1
    maxScore = max(scores.itervalues())
    if maxScore > ship.attacksLeft:
      maxScore = ship.attacksLeft
    return [pos for pos in options if scores[pos] >= maxScore]

  def minMove(self, options, ship):
    return listof(min, lambda pos: Vect.vectorize(pos, ship).magnitude, options)
    
  def canBeShot(self, options, ship):
    scores = {}
    for pos in options:
      scores[pos] = 0
      for attacker in self.theirShips:
        if attacker.canShoot(ship):
          scores[pos] += attacker.damage
    minScore = min(scores.itervalues())
    return [pos for pos in options if scores[pos] == minScore]

  def shipMove(self, ship):
    options = ship.cloud()
    for fun in [self.validPos, self.noMines, self.nearest, self.mostLethal, self.canBeShot, self.minSelfStack, self.minMove]:
      options = ship.listReduce(fun, options)
    move = random.choice(options)
    #print 'Movin', Vect.vectorize(ship, move).magnitude
    if move.x != ship.x or move.y != ship.y:
      ship.move(move.x, move.y)
      return True
    return False

  def shipShoot(self, ship):
    for target in sorted(self.theirShips, key=lambda ship: ship.health):
      if ship.canShoot(target):
        ship.attack(target)
        ship.targeted.add(target.id)
        if target.health <= 0:
          self.theirShips.remove(target)
  
  def command(self, ship):
    specials = {"Support": self.commandSupport,
             }
    try:
      specials[ship.type](ship)
    except KeyError:
      self.commandGeneral(ship)

  def commandGeneral(self, ship):
    while ship.movementLeft > 0:
      self.shipShoot(ship)
      if not self.shipMove(ship):
        break
    self.shipShoot(ship)

  def commandSupport(self, ship):
    options = ship.cloud()
    for fun in [self.validPos, self.noMines, self.clump, self.canBeShot, self.minSelfStack, self.minMove]:
      options = ship.listReduce(fun, options)
    move = random.choice(options)
    #print 'Movin', Vect.vectorize(ship, move).magnitude
    if move.x != ship.x or move.y != ship.y:
      ship.move(move.x, move.y)

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    print "Starting Turn", self.turnNumber, "of Round", self.roundNumber
    print [shipType.type for shipType in self.shipTypes]
    for ship in self.ships:
      ship.targeted = set()

    self.myShips = filter(lambda ship: ship.owner == self.playerID and ship.type != "Mine", self.ships)
    self.theirShips = filter(lambda ship: ship.owner != self.playerID and ship.type != "Mine", self.ships)
    self.myGate = (ship for ship in self.myShips if ship.type == "Warp Gate").next()
    self.theirGate = (ship for ship in self.theirShips if ship.type == "Warp Gate").next()
    
    self.myMines = [mine for mine in self.ships if mine.owner == self.playerID and mine.type == "Mine"]
    self.theirMines = [mine for mine in self.ships if mine.owner != self.playerID and mine.type == "Mine"]
    self.players[self.playerID].talk("I am player %i and it is currently turn %i of round %i"%(self.playerID, self.turnNumber, self.roundNumber))
    try:
      print self.score
    except AttributeError:
      self.score = (0, 0)
      self.nextRound()
    self.checkRoundWin()

    # Command the mines
    for mine in self.myMines:
      for target in self.theirShips:
        if Vect.vectorize(mine, target).magnitude <= mine.radius + target.radius:
          mine.selfDestruct()
          break

    # Purchasing
    
    for ship in self.myShips:
      self.command(ship)

    return True

  def __init__(self, conn):
      BaseAI.__init__(self, conn)
