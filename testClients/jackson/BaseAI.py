# -*- python -*-

from library import library

class BaseAI:
  """@brief A basic AI interface.

  This class implements most the code an AI would need to interface with the lower-level game code.
  AIs should extend this class to get a lot of builer-plate code out of the way
  The provided AI class does just that.
  """
  initialized = False
  iteration = 0
  runGenerator = None
  connection = None
  shipTypes = []
  players = []
  ships = []

  def startTurn(self):
    from GameObject import ShipType
    from GameObject import Player
    from GameObject import Ship

    BaseAI.shipTypes = [ShipType(library.getShipType(self.connection, i)) for i in xrange(library.getShipTypeCount(self.connection))]
    BaseAI.players = [Player(library.getPlayer(self.connection, i)) for i in xrange(library.getPlayerCount(self.connection))]
    BaseAI.ships = [Ship(library.getShip(self.connection, i)) for i in xrange(library.getShipCount(self.connection))]

    if not self.initialized:
      self.initialized = True
      self.init()
    BaseAI.iteration += 1;
    if self.runGenerator:
      try:
        return self.runGenerator.next()
      except StopIteration:
        self.runGenerator = None
    r = self.run()
    if hasattr(r, '__iter__'):
      self.runGenerator = r
      return r.next()
    return r
  
  def turnNumber(self):
    return library.getTurnNumber(self.connection)

  def playerID(self):
    return library.getPlayerID(self.connection)

  def gameNumber(self):
    return library.getGameNumber(self.connection)

  def round(self):
    return library.getRound(self.connection)

  def victoriesNeeded(self):
    return library.getVictoriesNeeded(self.connection)

  def innerMapRadius(self):
    return library.getInnerMapRadius(self.connection)

  def outerMapRadius(self):
    return library.getOuterMapRadius(self.connection)

  def __init__(self, connection):
    self.connection = connection
