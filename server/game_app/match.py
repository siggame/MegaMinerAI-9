from base import *
from matchUtils import *
from objects import *
import networking.config.config
from collections import defaultdict
from networking.sexpr.sexpr import *
import os
import itertools
import scribe
import random

Scribe = scribe.Scribe
#Initializes the cfgUnits file
cfgUnits = networking.config.config.readConfig("config/units.cfg")
for key in cfgUnits.keys():
  cfgUnits[key]['type'] = key

def loadClassDefaults(cfgFile = "config/defaults.cfg"):
  cfg = networking.config.config.readConfig(cfgFile)
  for className in cfg.keys():
    for attr in cfg[className]:
      setattr(eval(className), attr, cfg[className][attr])

class Match(DefaultGameWorld):
  def __init__(self, id, controller):
    self.id = int(id)
    self.controller = controller
    DefaultGameWorld.__init__(self)
    self.scribe = Scribe(self.logPath())
    self.addPlayer(self.scribe, "spectator")

    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id
    self.round = -1
    self.victoriesNeeded = self.victories
    self.mapRadius = self.radius

  def addPlayer(self, connection, type="player"):
    connection.type = type
    if len(self.players) >= 2 and type == "player":
      return "Game is full"
    if type == "player":
      self.players.append(connection)
      try:
        self.addObject(Player, [connection.screenName, self.startTime, 0, self.startEnergy])
      except TypeError:
        raise TypeError("Someone forgot to add the extra attributes to the Player object initialization")
    elif type == "spectator":
      self.spectators.append(connection)
      #If the game has already started, send them the ident message
      if (self.turn is not None):
        self.sendIdent([connection])
    return True

  def removePlayer(self, connection):
    if connection in self.players:
      if self.turn is not None:
        winner = self.players[1 - self.getPlayerIndex(connection)]
        self.declareWinner(winner, 'Opponent Disconnected')
      self.players.remove(connection)
    else:
      self.spectators.remove(connection)

  def start(self):
    if len(self.players) < 2:
      return "Game is not full"
    if self.winner is not None or self.turn is not None:
      return "Game has already begun"    
   
    self.turn = self.players[-1]
    self.turnNumber = -1
    self.nextRound()
    self.nextTurn()
    self.ordering = ["radius", "type", "maxAttacks", "maxMovement", "maxMovement", "maxAttacks", "damage", 
                     "range", "maxHealth", "maxHealth"]
    self.warpGate = [cfgUnits["Warp Gate"][value] for value in self.ordering]
    self.spawnableTypes = cfgUnits.keys()
    self.spawnableTypes.remove("Warp Gate")
    self.spawnableTypes.remove("Mine")
    self.shipChain = []
    return True

  def nextRound(self):
    self.round += 1
    #Handles logic for starting a new round:
      #first get rid of all shiptypes and ships available that round, then put into a new subset of available ship types
    print "YOU ARE ENTERING A NEW ROUND", self.round

    for obj in self.objects.values():
      if isinstance(obj, ShipType) or isinstance(obj, Ship):
        self.removeObject(obj)

    for player in self.objects.players:
      #Give players energy initially each round
      player.energy = self.startEnergy
      player.warpGate = self.addObject(Ship, [player.id, (player.id * 2 - 1) * self.mapRadius / 2, 0] + self.warpGate).id
    
    # Ensure you have at least 4 ships in the chain
    if len(self.shipChain) < 4:
      # Add a random permutation of the types to the chain
      random.shuffle(self.spawnableTypes)
      self.shipChain += self.spawnableTypes
    # use the next 4
    using, self.shipChain = self.shipChain[:4], self.shipChain[4:]
    for shipType in using:
      self.addObject(shipType, [shipType, cfgUnits[shipType]["cost"]])

    return True

  def nextTurn(self):
    self.turnNumber+=1
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0
    else:
      return "Game is over." 
      
    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()

    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    self.animations = ["animations"]
    return True

  def checkRoundWinner(self):
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]
    gates = [player.warpGate for player in self.objects.players]
    if len(gates) < 2:
      if len(gates) == 1:
        if player1.warpGate in self.objects:
          player2.victories += 1
        else:
          player1.victories += 1
      else: # Both win if they both die in one turn
        player1.victories += 1
        player2.victories += 1
      self.nextRound()
    elif self.turnNumber >= self.turnLimit:
      # Warp gate health
      if self.objects[player1.warpGate].health > self.objects[player2.warpGate].health:
        player1.victories += 1
      elif self.objects[player1.warpGate].health < self.objects[player2.warpGate].health:
        player2.victories += 1
      else:
        # score
        scores = [player1.energy, player2.energy]
        for ship in self.objects.ships:
          scores[ship.owner] += cfgUnits[ship.type]["cost"]
        for player in self.objects.players:
          for ship in player.warping:
            scores[ship.owner] += cfgUnits[ship.type]["cost"]
        if scores[0] > scores[1]:
          player1.victories += 1
        elif scores[0] < scores[1]:
          player2.victories += 1
        else:
          player1.victories += 1
          player2.victories += 1
      self.nextRound()
    
  def checkWinner(self):
    self.checkRoundWinner()
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]
    if player1.victories >= self.victories and player1.victories > player2.victories:
      self.declareWinner(player1, "Decisive")
    elif player2.victories >= self.victories and player2.victories > player1.victories:
      self.declareWinner(player2, "Decisive")
    elif player1.victories >= self.victories and player2.victories >= self.victories:
      self.declareWinner(random.choice(self.objects.players), "Luck")

  def declareWinner(self, winner, reason=''):
    #TODO give reasons for winning, who has more round victories, etc..
    self.winner = winner

    msg = ["game-winner", self.id, self.winner.user, self.getPlayerIndex(self.winner), reason]
    self.scribe.writeSExpr(msg)
    self.scribe.finalize()
    self.removePlayer(self.scribe)

    for p in self.players + self.spectators:
      p.writeSExpr(msg)

    self.sendStatus([self.turn])
    self.playerID ^= 1
    self.sendStatus([self.players[self.playerID]])
    self.playerID ^= 1
    self.turn = None
    
  def logPath(self):
    return "logs/" + str(self.id) + ".glog"

  @derefArgs(Player, None)
  def talk(self, object, message):
    return object.talk(message, )

  @derefArgs(Ship, None, None)
  def move(self, object, x, y):
    return object.move(x, y,)

  @derefArgs(Ship)
  def selfDestruct(self, object):
    return object.selfDestruct()

  @derefArgs(Ship, Ship)
  def attack(self, object, target):
    return object.attack(target, )

  @derefArgs(ShipType, None, None)
  def warpIn(self, object, x, y):
    return object.warpIn(x, y, )


  def sendIdent(self, players):
    if len(self.players) < 2:
      return False
    list = []
    for i in itertools.chain(self.players, self.spectators):
      list += [[self.getPlayerIndex(i), i.user, i.screenName, i.type]]
    for i in players:
      i.writeSExpr(['ident', list, self.id, self.getPlayerIndex(i)])

  def getPlayerIndex(self, player):
    try:
      playerIndex = self.players.index(player)
    except ValueError:
      playerIndex = -1
    return playerIndex

  def sendStatus(self, players):
    for i in players:
      i.writeSExpr(self.status(i))
      i.writeSExpr(self.animations)
    return True


  def status(self, connection):
    msg = ["status"]

    msg.append(["game", self.turnNumber, self.playerID, self.gameNumber, self.round, self.victoriesNeeded, self.mapRadius])

    typeLists = []
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Ship"] + [i.toList() for i in self.objects.values() if i.__class__ is Ship and 
                     (not i.stealthed or i.owner == self.playerID or connection.type != "player"])
    typeLists.append(["ShipType"] + [i.toList() for i in self.objects.values() if i.__class__ is ShipType])

    msg.extend(typeLists)

    return msg


loadClassDefaults()

