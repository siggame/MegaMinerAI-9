import math
import networking.config.config
#Initializes the cfgUnits file
cfgUnits = networking.config.config.readConfig("config/units.cfg")
def distance(fromX, toX, fromY, toY):
  return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))

def inRange(x1, y1, rad1, x2, y2, rad2):
  return distance(x1, x2, y1, y2) <= rad1 + rad2

class Player:
  def __init__(self, game, id, playerName, time, victories, energy):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.victories = victories
    self.energy = energy

  def toList(self):
    value = [
      self.id,
      self.playerName,
      self.time,
      self.victories,
      self.energy,
      ]
    return value

  def nextTurn(self):
    pass
    # If it's your turn and it isn't after the last turn, you get some energy (Maybe)
    #if self.id == self.game.playerID:
      #if self.game.turnNumber < self.game.turnLimit:
        #self.energy += 50

  def talk(self, message):
    #TODO: talk..look off past megaminers, very similar
    pass



class Ship:
  def __init__(self, game, id, owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, range, health, maxHealth):
    self.game = game
    self.id = id
    self.owner = owner
    self.x = x
    self.y = y
    self.radius = radius
    self.type = type
    self.attacksLeft = attacksLeft
    self.movementLeft = movementLeft
    self.maxMovement = maxMovement
    self.maxAttacks = maxAttacks
    self.damage = damage
    self.range = range
    self.health = health
    self.maxHealth = maxHealth

  def toList(self):
    value = [
      self.id,
      self.owner,
      self.x,
      self.y,
      self.radius,
      self.type,
      self.attacksLeft,
      self.movementLeft,
      self.maxMovement,
      self.maxAttacks,
      self.damage,
      self.range,
      self.health,
      self.maxHealth,
      ]
    return value

  def nextTurn(self):
    if self.owner == self.game.playerID:
      self.movementLeft = self.maxMovement
    else:
      self.movementLeft = 0

  def move(self, x, y):
    print x, "  ", y
    #moved is the distance they've moved, where they were to where they're going
    moved = distance(self.x, x, self.y, y)       
    #if they're trying to move outside the map
    if x**2 + y**2 > self.game.mapRadius**2:
      return "You don't want to move out of the map, you'd be lost in Space"
    #check if they can'at move that far
    elif self.movementLeft - moved < 0:
      return "You cannot move that far, your engines lack the power"#think of something clever here
    #have to move somewhere..yeah.
    elif moved == 0:
      return "Must move somewhere"
    
    #successful move, yay! 
    self.game.animations.append(['move', self.x, self.y, x, y, self]) #move animation for those visualizer guys
    self.x = x
    self.y = y
    self.movementLeft -= moved
    #Check to see if they moved onto a mine, TWAS A TRAP!
    for unit in self.game.objects.ships:
      if unit.owner != self.owner: 
        if unit.type == "Mine": 
          if inRange(x,y,self.radius,unit.x,unit.y,unit.radius):
            #If a mine in range, hit the unit that moved there and destroy the mine
            self.health -= unit.damage
            self.game.removeObject(unit)
            if self.health <= 0:
              self.game.removeObject(self)
    return True

  def selfDestruct(self):
    for target in self.objects.ships:
      if inRange (self.x, self.y, self.radius,target.x, target.y, target.radius):
        if target.owner != self.owner:
          #TODO placeholder value
          attack(target) 

  def attack(self, target):
    #TODO: A lot of things. 
    #TODO: cannot attack same target >1 per turn. (can make a set of possible targets, and remove target each time)
    #TODO: Figure out how to get things from the config
    #if ConfigSectionMap("Fighter")['name'] == "fighter":
      #print ConfigSectionMap("Fighter")['name']
    
    #make sure attack is not invalid
    if self.attacksLeft <= 0:
      return 'You have no attacks left'
    elif target.owner == self.owner:
      return 'No friendly fire please'
    elif not self.inRange (self, target):
      return "Target too far away"
                     
    #TODO Make sure the type for mine layer matches up with the logic
    #Handles attacks for the mine layer
    #Minelayer attacks self to drop a mine at its center
    if self.type == "mineLayer" and self.id == target.id:
      ##TODO Plug in data here for the "Mine" ship
      self.game.addObject(Ship(owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, health, maxHealth))
      self.attacksLeft -= 1
    else:
      modifier = 1
      #Checking to see if a radar is in range of the target
      for unit in self.objects.ships:
        if unit.owner == self.owner:
          if unit.type == "radar":
            if self.inRange(unit,target):
            #Increment the damage modifier for each radar in range
              modifier+=unit.damage*.1
      self.game.animations.append(['attack', self, target])
      target.health-=self.damage*modifer
      self.attacksLeft -= 1
      if target.health <= 0:
        self.game.removeObject(target)
    
  def inRange(self, target):
    return inRange(self.x, self.y, self.range, target.x, target.y, target.range)


class ShipType:
  def __init__(self, game, id, type, cost):
    self.game = game
    self.id = id
    self.type = type
    self.cost = cost

  def toList(self):
    value = [
      self.id,
      self.type,
      self.cost,
      ]
    return value

  def nextTurn(self):
    pass

  def warpIn(self, x, y):
    #check to see whose turn it is, hint: it's player's turn
    if self.game.turnNumber == 0:
      player = self.game.objects.players[0]
    else:
      player = self.game.objects.players[self.game.turnNumber%2]
    #TODO (Maybe) Try to build library of ships each turn to speed up calculations (last priority)
    warpX = 0; warpY = 0
    for ship in self.game.objects.values():
      if isinstance(ship,Ship): #if ship is a Ship
        if ship.type == "Warp Gate" and ship.owner == self.game.playerID:
          warpX = ship.x
          warpY = ship.y
    if self.game.playerID != player.id:
      return "You cannot warp in ships on your opponent's turn"
    if x**2 + y**2 > self.game.mapRadius**2:
      return "That ship would be lost in space...forever"
    elif player.energy < self.cost:
      return "You need to not be poor to buy that kind of ship"
    elif not inRange(warpX,warpY,cfgUnits["Warp Gate"]["range"],x,y,0) and self.type != "FTL":
      return "You must spawn that ship closer to your Warp Gate"
    else:    
      #spawn the unit with its stats, from units.cfg in config directory
      print self.type, "ship spawned for player", self.game.playerID
      self.game.addObject(Ship,[self.game.playerID, x, y, 
      cfgUnits[self.type]["radius"], self.type, 
      cfgUnits[self.type]["maxAttacks"], 
      cfgUnits[self.type]["maxMovement"], 
      cfgUnits[self.type]["maxMovement"], 
      cfgUnits[self.type]["maxAttacks"], 
      cfgUnits[self.type]["damage"], 
      cfgUnits[self.type]["radius"],
      cfgUnits[self.type]["maxHealth"], 
      cfgUnits[self.type]["maxHealth"]
      ])
      player.energy -= self.cost
  
    


