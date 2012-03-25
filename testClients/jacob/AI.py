#-*-python-*-
from BaseAI import BaseAI


class ShipUsage:
  def __init__(self, offense, defense, support, worth=1):
    self.defense = 0
    self.offense = 0
    self.support = 0
    self.worth = 1


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
    self.usageTable = {}

  ##This function is called once, after your last turn
  def end(self):
    pass

  def initTurn(self):
    self.me = self.players[self.playerID]
    self.fleet = [i for i in self.ships if i.owner == self.playerID]
    self.enemies = [i for i in self.ships if i.owner != self.playerID]
    self.warpGate = self.fleet[0]

  def buyShip(self):
    for i in self.shipTypes:
      print i.type, i.cost

    print '-------------'

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    self.initTurn()
    if self.turnNumber < 2:
      self.buyShip()
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
