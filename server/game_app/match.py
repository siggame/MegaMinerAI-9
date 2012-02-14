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

    self.turnNumber = -1
    self.playerID = -1
    self.gameNumber = id
    self.round = -1
    self.victoriesNeeded = self.victories
    self.mapRadius = self.radius
    self.stealthShips = []

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
    self.round += 1
    #Handles logic for starting a new round:
      #first get rid of all shiptypes and ships available that round, then put into a new subset of available ship types
    print "YOU ARE ENTERING A NEW ROUND", self.round
    for i in self.objects.values():
      if isinstance(i,ShipType) or isinstance(i,Ship):
        self.removeObject(i)
    for player in self.objects.players:
      #dirmod = directional modifier, where warp gate spawns for each player
      
      #Give players more energy initially each round
      player.energy = 75+self.round*25
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
    
    #types are list of all ships, want to remove warp and mine from it before assigning what ships are available
    Types = cfgUnits.keys()
    Types.remove("Warp Gate")
    Types.remove("Mine") 
    i = 0
    #add random ship types from map, remove that ship type to avoid duplicates
    while i < 4:
      rand = random.randrange(0,len(Types))
      name=Types[rand]
      cost=cfgUnits[name]["cost"]     
      self.addObject(ShipType,[name,cost])
      Types.remove(Types[rand])
      i += 1
    #pass

  def nextTurn(self):
    for ship in self.objects.ships:
      ship.endTurn()  
      
    if self.turn == self.players[0]:
      self.turn = self.players[1]
      self.playerID = 1
    elif self.turn == self.players[1]:
      self.turn = self.players[0]
      self.playerID = 0
    else:
      return "Game is over." 
    self.turnNumber += 1
    
   #TODO MOAR stealth ship stuff     
   # for ship in self.stealthShips:
    #  if ship.owner == self.playerID:
    #    self.addObject(Ship,[self.playerID,ship.x, ship.y, ship.radius, ship.type, ship.maxAttacks,
     #   ship.maxMovement,ship.maxMovement,ship.maxAttacks,ship.damage,ship.range,
    #    ship.maxHealth,ship.maxHealth])
      
    for obj in self.objects.values():
      obj.nextTurn()
    self.checkWinner()
    #determine when a new round should start. NEVER MOD BY 0, makes computer not happy. >_<
    if self.turnNumber == 0:
      self.nextRound()
    else: 
      if self.turnNumber%self.turnLimit == 0 and self.winner is None:
        self.turnNumber = 0
        self.nextRound()
    if self.winner is None:
      self.sendStatus([self.turn] +  self.spectators)
    else:
      self.sendStatus(self.spectators)
    self.animations = ["animations"]
    return True

  def checkWinner(self):
    player1 = self.objects.players[0]
    player2 = self.objects.players[1]
    #Each turn victory check: Is a warp gate dead?
    for ship in self.objects.ships:
      if ship.type == "Warp Gate" and ship.health <= 0:
        if ship.owner == 0:
          print self.objects.players[1].playerName + " wins the round!"
          self.players[1].victories += 1
        else:
          print self.objects.players[0].playerName + " wins the round!"
          self.players[0].victories += 1
          
    #Turn limit victory checks
    if self.turnNumber%self.turnLimit == 0:
      warpHealth =-1
      #TODO: THIS LOGIC IS BROKEN! CHECK TO SEE IF A PLAYER DOES NOT HAVE A WARP GATE INSTEAD
      for ship in self.objects.ships:
        if ship.type == "Warp Gate" and warpHealth == -1:
          warpHealth = ship.health
        elif ship.type == "Warp Gate" and warpHealth != -1:
          if ship.health < warpHealth:
            if ship.owner == 0:
              print self.objects.players[1].playerName + " wins the round!"
              self.objects.players[1].victories += 1
            else:
              print self.objects.players[0].playerName + " wins the round!"
              self.objects.players[0].victories += 1
          elif ship.health > warpHealth:
            if ship.owner == 1:
              print self.objects.players[1].playerName + " wins the round!"
              self.objects.players[1].victories += 1
            else:
              print self.objects.players[0].playerName + " wins the round!"
              self.objects.players[0].victories += 1
          #If warp gates have equal health, we compare the overall value of the players
          else:
            player0Val = self.objects.players[0].energy
            player1Val = self.objects.players[1].energy
            for obj in self.objects.ships:
              if obj.owner == 0:
                player0Val += cfgUnits[obj.type]["cost"]
              else:
                player1Val += cfgUnits[obj.type]["cost"]
            if player0Val > player1Val:
              print self.objects.players[0].playerName + " wins the round!"
              self.objects.players[0].victories += 1
            elif player0Val < player1Val:
              print self.objects.players[1].playerName + " wins the round!"
              self.objects.players[1].victories += 1
            else:
              print "The round is a tie!"
              self.objects.players[0].victories += 1             
              self.objects.players[1].victories += 1
     #TODO Make better declarewinner statement
    count = 0
    for player in self.objects.players:
      if player.victories == self.victoriesNeeded:
        self.declareWinner(self.players[count],"player.playerName +  has won the game!")
        break
      count+=1
              
                

  def declareWinner(self, winner, reason=''):
  #TODO give reasons for winning, who has more round victories, etc..
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

