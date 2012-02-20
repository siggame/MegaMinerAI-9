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
    self.warping = []
    self.warpGate = 0

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

  def talk(self, message):
    #TODO: talk..look off past megaminers, very similar. NEED TALK ANIMATION
    #self.game.animations.append(['Player-Talk', self.id, message])
    #return True
    pass


class Ship:
  def __init__(self, game, id, owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, range, health, maxHealth, selfDestructDamage):
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
    self.selfDestructDamage = selfDestructDamage
    self.stealthed = False

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
      self.selfDestructDamage,
      ]
    return value

  def nextTurn(self):
    #TODO: MAKE UNITS WARP IN AT START OF NEXT TURN
    #Healing other ships in range of engineering ship      
    if self.owner != self.game.playerID and self.type == "Engineering":
      for unit in self.game.objects.ships:
        if self.owner == unit.owner:
          if self.inRange(unit):
            unit.health += unit.maxHealth * self.damage / 100.0
            if unit.health > unit.maxHealth:
              unit.health = unit.maxHealth

    #TODO: Make sure minelayers don't get attacks replenished
    if self.owner == self.game.playerID:
      if self.movementLeft == -1 and self.attacksLeft == -1:
        self.movementLeft = 0
        self.attacksLeft = 0
      else:
        self.movementLeft = self.maxMovement         
        self.attacksLeft = self.maxAttacks
                    
  def move(self, x, y):
    if self.owner != self.game.playerID:
      return "you cannot move your oppenents ships"
    #moved is the distance they've moved, where they were to where they're going
    moved = distance(self.x, x, self.y, y)       
    #if they're trying to move outside the map
    if x**2 + y**2 > self.game.mapRadius**2:
      return "You don't want to move out of the map, you'd be lost in Space"
    #check if they can't move that far
    elif self.movementLeft - moved < 0:
      return "You cannot move that far, your engines lack the power"#think of something clever here
    #have to move somewhere..yeah.
    elif moved == 0:
      return "Must move somewhere"
    
    #successful move, yay! 
    self.game.animations.append(['move', self.x, self.y, x, y, self.id]) #move animation for those visualizer guys
    self.x = x
    self.y = y
    self.movementLeft -= moved
    
    #Check to see if they moved onto a mine, TWAS A TRAP!
    for unit in self.game.objects.ships:
      if unit.owner != self.owner and unit.type == "Mine": 
        if inRange(x,y,self.radius,unit.x,unit.y,unit.radius):
          #If a mine in range, hit the unit that moved there and destroy the mine
          self.health -= unit.damage
          self.game.removeObject(unit)
          self.game.animations.append(['attack',unit.id,self.id])
          if self.health <= 0:
            pass
            #TODO: Makes mines kill enemy ships
#           self.game.removeObject(self)
    return True

  def selfDestruct(self):
    #TODO: NO SPLODEY FOR WARP GATES
    if self.owner == self.game.playerID:
      return "The enemy ship refuses to blow itself up, sorry"
    for target in self.game.objects.ships:
      if inRange (self.x, self.y, self.radius,target.x, target.y, target.radius):
        if target.owner != self.owner:
          #TODO: MAKE NOT ATTACK - SOMETHING UNIQUE
          #TODO: Make Kamakizes (too lazy to check spelling) really good at exploding
          self.attack(target)   
          self.game.removeObject(self)
          self.game.animations.append(['selfDestruct', self.id])
    return True
    
  def attack(self, target):
        
    #TODO: cannot attack same target >1 per turn.
      #(can make a set of possible targets, and remove target each time)
    modifier = 1
    #TODO: MAKE SURE NO ATTACK MINES
    if self.owner != self.game.playerID:
       return "You cannot make enemy ships attack"
    if self.attacksLeft <= 0:
      return 'You have no attacks left'
    if self.type == "Mine Layer" and self.id == target.id:
      self.game.addObject(Ship,[self.game.playerID, self.x, self.y, 
      cfgUnits["Mine"]["radius"], "Mine", 
      cfgUnits["Mine"]["maxAttacks"], 
      cfgUnits["Mine"]["maxMovement"], 
      cfgUnits["Mine"]["maxMovement"], 
      cfgUnits["Mine"]["maxAttacks"], 
      cfgUnits["Mine"]["damage"], 
      cfgUnits["Mine"]["radius"],
      cfgUnits["Mine"]["maxHealth"], 
      cfgUnits["Mine"]["maxHealth"],
      cfgUnits["Mine"]["selfDestructDamage"],
      ])
      self.attacksLeft -= 1
      return True
    elif target.owner == self.owner:
      return 'No friendly fire please'
    elif not self.inRange(target):
      return "Target too far away"           
    else:       
      #Checking to see if a radar is in range of the target
      for unit in self.game.objects.ships:
        if unit.owner == self.owner:
          if unit.type == "Radar":
            if unit.inRange(target):
            #Increment the damage modifier for each radar in range
              modifier+=.5
      if self.type == "EMP":
        for unit in self.game.objects.ships:
          if unit.owner != self.owner:
            if self.inRange(unit):
              unit.attacksLeft = -1
              unit.movementLeft = -1
              self.attacksLeft = -1
              self.movementLeft = -1
              
      self.game.animations.append(['attack', self.id, target.id])
      target.health-=self.damage*modifier
      self.attacksLeft -= 1
      if target.health <= 0:
        self.game.removeObject(target)
    return True 
    
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
      print self.game.playerID, player.id
      return "You cannot warp in ships on your opponent's turn",
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
      cfgUnits[self.type]["maxHealth"],
      cfgUnits[self.type]["selfDestructDamage"]
      ])
      player.energy -= self.cost
    return True
    


