#-*-python-*-
from BaseAI import BaseAI
#from random import shuffle


class ShipUsage:
  def __init__(self, offense, defense, support, cost=0, worth=1):
    self.defense = defense
    self.offense = offense
    self.support = support
    self.cost = cost
    self.worth = worth


class FleetTable:
  def __init__(self, fleet):
    if fleet == None:
      self.fleet = {
          'offense': 100,
          'defense': 100,
          'support': 100
          }
    else:
      self.fleet = fleet

  def __sub__(self, rhs):
    pass
    #fleet

  def __add__(self, rhs):
    pass

# Should help us prioritize our purchases
usageTable = {
    'Battleship': ShipUsage(25, 5, 0, 25, 1),
    'Juggernaut': ShipUsage(5, 20, 0, 15, 1),
    'Mine Layer': ShipUsage(1, 5, 20, 5, 1),
    'Support': ShipUsage(0, 5, 20, 5, 1),
    'EMP': ShipUsage(6, 6, 6, 5, 1),
    'Stealth': ShipUsage(20, 2, 4, 5, 1),
    'Cruiser': ShipUsage(15, 5, 0, 15, 1),
    'Weapons Platform': ShipUsage(10, 13, 0, 15, 1),
    'Interceptor': ShipUsage(3, 7, 0, 2, 1),
    'Bomber': ShipUsage(7, 3, 0, 2, 1),
    'Mine': ShipUsage(0, 0, 0, 0, 0)
    }

retaliationTable = {
    'Battleship': ShipUsage(25, 5, 5),
    'Juggernaut': ShipUsage(5, 25, 10),
    'Mine Layer': ShipUsage(10, -1, 1),
    'Support': ShipUsage(15, 2, 0),
    'EMP': ShipUsage(15, 0, 0),
    'Stealth': ShipUsage(2, 10, 3),
    'Cruiser': ShipUsage(2, 15, 2),
    'Weapons Platform': ShipUsage(30, 1, 10),
    'Interceptor': ShipUsage(0, 10, 2),
    'Bomber': ShipUsage(0, 10, 2),
    'Mine': ShipUsage(0, 0, 1)
    }


class Enemy:
  def __init__(self):
    self.energy = 50
    # Dictionary indexed by id of the enemies ships in this round
    self.shipIds = []
    self.ships = {}
    # The the ids of the ships that are dead.
    self.dead = []
    self.stealth = []
    self.unknown = 0

  def modifyFleet(self, desiredFleet, multiplier):
    pass

  def addShip(self, ship, desiredFleet):
    if ship.id not in self.shipIds:
      if ship.type == 'Stealth':
        self.stealth.append(ship.id)
      if ship.type != 'Warp Gate':
        self.energy -= usageTable[ship.type].cost
      else:
        self.warpGate = ship

      self.shipIds.append(ship.id)

    self.ships[ship.id] = ship

  def killShip(self, ship, desiredFleet):
    del self.ships[ship.id]

    return self.modifyFleet(desiredFleet, -1)


class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "dev_applejack"

  @staticmethod
  def password():
    return "gNJrtJ"

  ##This function is called once, before your first turn
  def init(self):
    self.maxBuys = 2

  ##This function is called once, after your last turn
  def end(self):
    pass

  def roundInit(self):
    self.perfectFleet = {
        'offense': 100,
        'defense': 100,
        'support': 100
        }
    self.enemy = Enemy()

  def initTurn(self):
    self.me = self.players[self.playerID]
    self.you = self.players[1 - self.playerID]
    self.fleet = [i for i in self.ships if i.owner == self.playerID]
    self.enemies = [i for i in self.ships if i.owner != self.playerID]

    for i in self.enemies:
      self.perfectFleet = self.enemy.addShip(i, self.perfectFleet)

    for i in self.fleet:
      if i.type == 'Warp Gate':
        self.warpGate = i

    self.target = self.enemy.warpGate

  def buyShip(self):
    for i in self.shipTypes:
      pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    if self.turnNumber < 2:
      self.roundInit()
    self.initTurn()
    if self.you.energy != self.enemy.energy and self.turnNumber > 2:
      self.enemy.unknown = (self.enemy.energy - self.you.energy) / 5

    move = self.distance(self.warpGate.x, self.warpGate.y, self.target.x, self.target.y)
    if move > self.warpGate.movementLeft:
      move = self.warpGate.movementLeft

    pt = self.pointOnLine(self.warpGate.x, self.warpGate.y, self.target.x, self.target.y, move)

    self.warpGate.move(pt[0], pt[1])
    self.me.talk("I WANT HUGS!!")

    self.buyShip()

    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
