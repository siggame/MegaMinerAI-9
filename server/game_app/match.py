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

    #TODO: INITIALIZE THESE!
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
    self.nextTurn()
    return True

  def nextRound(self):
    print "YOU ARE ENTERING A NEW ROUND", self.round
    for i in self.objects.values():
      if isinstance(i,ShipType) or isinstance(i,Ship):
        self.removeObject(i)
    for player in self.objects.players:
      player.energy = 100
      dirmod = 1
      if player.id == 1:
        dirmod = -1   
      self.addObject(Ship,[player.id, (self.mapRadius/2)*dirmod, (self.mapRadius/2)*dirmod, 
        cfgUnits["Warp Gate"]["radius"], 
        "Warp Gate", 
        cfgUnits["Warp Gate"]["maxAttacks"], 
        cfgUnits["Warp Gate"]["maxMovement"], 
        cfgUnits["Warp Gate"]["maxMovement"], 
        cfgUnits["Warp Gate"]["maxAttacks"], 
        cfgUnits["Warp Gate"]["damage"], 
        cfgUnits["Warp Gate"]["range"],
        cfgUnits["Warp Gate"]["maxHealth"], 
        cfgUnits["Warp Gate"]["maxHealth"]
        ])
    
    self.round += 1
    Types = cfgUnits.keys()
    Types.remove("Warp Gate")
    Types.remove("Mine") 
    i = 0
    while i < 4:
      rand = random.randrange(0,len(Types))
      name=Types[rand]
      cost=cfgUnits[name]["cost"]     
      self.addObject(ShipType,[name,cost])
      Types.remove(Types[rand])
      i += 1
    pass

  def nextTurn(self):
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0
    else:
      return "Game is over." 
    self.turnNumber += 1
    if self.turnNumber == 0:
      self.nextRound()
    else: 
      if self.turnNumber%self.turnLimit == 0:
        self.turnNumber = 0
        self.nextRound()

    for obj in self.objects.values():
      obj.nextTurn()

    self.checkWinner()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    self.animations = ["animations"]
    return True

  def checkWinner(self):
    #TODO: Check if a player has won the round.
    if self.round == 5:
      self.declareWinner (self.players[0],"I said so")
    for ship in self.objects.values():
      if isinstance(ship,Ship) and ship.type == "Warp Gate":
        if ship.health <= 0:
          pass
        #TODO: Make the other player win
    #TODO: Make this check if a player won the match, and call declareWinner with a player if they did
    pass

  def declareWinner(self, winner, reason=''):
    print "Player", self.getPlayerIndex(self.winner), "wins game", self.id
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
    return object.move(x, y, )

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
      i.writeSExpr(self.status())
      i.writeSExpr(self.animations)
    return True


  def status(self):
    msg = ["status"]

    msg.append(["game", self.turnNumber, self.playerID, self.gameNumber, self.round, self.victoriesNeeded, self.mapRadius])

    typeLists = []
    typeLists.append(["Player"] + [i.toList() for i in self.objects.values() if i.__class__ is Player])
    typeLists.append(["Ship"] + [i.toList() for i in self.objects.values() if i.__class__ is Ship])
    typeLists.append(["ShipType"] + [i.toList() for i in self.objects.values() if i.__class__ is ShipType])

    msg.extend(typeLists)

    return msg


loadClassDefaults()

