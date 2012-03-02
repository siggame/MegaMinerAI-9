import math
import networking.config.config
#Initializes the cfgUnits file
#Initializes the cfgUnits file
cfgUnits = networking.config.config.readConfig("config/units.cfg")
for key in cfgUnits.keys():
  cfgUnits[key]['type'] = key
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
    self.game.animations.append(['playerTalk', self.id, message])
    return True


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
    self.targeted = set()

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
    
  def allInRange(self, owner, range = None):
    result = []
    if range == None:
      range = self.range
    for ship in self.game.objects.ships:
      if ship.owner == owner and inRange(self.x, self.y, range, ship.x, ship.y, ship.radius):
        result.append(ship)
    return result

  def nextTurn(self):
    #Ships warp in at the beginning of that player's turn
    for warp in self.game.objects.players[self.game.playerID].warping:
      shipStats = [cfgUnits[warp[0]][value] for value in self.game.ordering]   
      self.game.addObject(Ship, [self.game.playerID, warp[1], warp[2]] + shipStats)
      self.game.objects.players[self.game.playerID].warping.remove(warp)

    #Healing other ships in range of support ship      
    self.targeted = set()
    #Healing other ships in range of engineering ship      
    if self.owner != self.game.playerID and self.type == "Support":
      for healed in self.allInRange(self.owner):
        healed.health += healed.maxHealth * self.damage / 100.0
        if healed.health > healed.maxHealth:
          healed.health = healed.maxHealth

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
        if inRange(x,y,self.radius,unit.x,unit.y,unit.range):
          for attacked in ship.allInRange(self.owner):
            attacked.health -= unit.damage
            self.game.animations.append(['attack', unit, attacked])
            if attacked.health <= 0:
              self.game.removeObject(attacked)
          self.game.removeObject(unit)
    return True

  def selfDestruct(self):
    #Done, need to check. TODO: NO SPLODEY FOR WARP GATES
    if self.type == "Warp Gate":
      return "You cannot explode your Warp Gate"
    if self.owner != self.game.playerID:
      return "The enemy ship refuses to blow itself up, sorry"
    for target in self.game.objects.ships:
      if inRange (self.x, self.y, self.radius,target.x, target.y, target.radius):
        if target.owner != self.owner:
          self.attack(target)   
          self.game.removeObject(self)
          self.game.animations.append(['selfDestruct', self.id])
    return True
    
  def attack(self, target):
        
    #TODO: cannot attack same target >1 per turn.
      #(can make a set of possible targets, and remove target each time)
    if target.type == "Mine":
      return "You cannot attack mines"
    modifier = 1
    #DONE? need to check TODO: MAKE SURE NO ATTACK MINES
    if self.owner != self.game.playerID:
       return "You cannot make enemy ships attack"
    if self.attacksLeft <= 0:
      return 'You have no attacks left'
    if target.id in self.targeted:
      return "You have already commaned %i to attack %i"%(self.id, target.id)
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
      self.maxAttacks -= 1
      return True
    elif target.owner == self.owner:
      return 'No friendly fire please'
    elif not self.inRange(target):
      return "Target too far away"           
    else:       
      #Checking to see if a radar is in range of the target
      for unit in self.game.objects.ships:
        if unit.owner == self.owner:
          if unit.type == "Support":
            if unit.inRange(target):
            #Increment the damage modifier for each radar in range
              modifier+=.5
      if self.type == "EMP":
        self.maxAttacks -= 1
        for unit in self.game.objects.ships:
          if unit.owner != self.owner:
            if self.inRange(unit):
              unit.attacksLeft = -1
              unit.movementLeft = -1
              
      self.game.animations.append(['attack', self.id, target.id])
      target.health-=self.damage*modifier
      self.attacksLeft -= 1
      if target.health <= 0:
        self.game.removeObject(target)
    self.targeted.add(target.id)
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
    #TODO make units warp in at start of next turn
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
      #print self.game.playerID, player.id
      return "You cannot warp in ships on your opponent's turn",
    if x**2 + y**2 > self.game.mapRadius**2:
      return "That ship would be lost in space...forever"
    elif player.energy < self.cost:
      return "You need to not be poor to buy that kind of ship"
    elif not inRange(warpX,warpY,cfgUnits["Warp Gate"]["range"],x,y,0) and self.type != "FTL":
      return "You must spawn that ship closer to your Warp Gate"
    else:    
      #spawn the unit with its stats, from units.cfg in config directory
      #Add unit to queue to be warped in at the beginning of this player's next turn
      self.game.objects.players[self.game.playerID].warping.append([self.type,x,y])
      player.energy -= self.cost
    return True
    


