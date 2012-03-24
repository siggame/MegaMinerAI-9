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
    self.isStealthed = False
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
      #Uses a list of ship values in the config to get all of the ships stats
      shipStats = [cfgUnits[warp[0]][value] for value in self.game.ordering] 
      #Adds the ship with the retreived stats to the game
      self.game.addObject(Ship, [self.game.playerID, warp[1], warp[2]] + shipStats)
      #Remove the created ship from the queue
      self.game.objects.players[self.game.playerID].warping.remove(warp)
                                                                                            
    
    #Healing other ships in range of support ship      
    self.targeted = set()
    #Healing other ships in range of engineering ship      
    if self.owner != self.game.playerID and self.type == "Support":
      for healed in self.allInRange(self.owner):
        if healed.id != self.id:
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
      if self.type == "Stealth" and self.owner == self.game.playerID:
        self.isStealthed = True
                    
  def move(self, x, y):
    if self.owner != self.game.playerID:
      return "you cannot move your oppenent's %s %i "%(self.type,self.id)
    #moved is the distance they've moved, where they were to where they're going
    moved = distance(self.x, x, self.y, y)       
    #if they're trying to move outside the map
    if distance(0,x,0,y) + self.radius > self.game.outerMapRadius:
      return "We're deep in Space, corner of No and Where. You take extra care to not move your %s %i out of the map."%(self.type,self.id)
    #check if they can't move that far
    elif self.movementLeft - moved < 0:
      return "You cannot move your %s %i %i spaces away."%(self.type,self.id,moved)#think of something clever here
    #have to move somewhere..yeah.
    elif moved == 0:
      return "Must move your %s %i somewhere"%(self.type,self.id)
    
    #successful move, yay! 
    self.game.animations.append(['move', self.id, self.x, self.y, x, y]) #move animation for those visualizer guys
    self.x = x
    self.y = y
    self.movementLeft -= moved
    
    #Moved to next turn
    #Check to see if they moved onto a mine, TWAS A TRAP!#
#    radius = self.radius
#    for mine in self.game.objects.ships:
#      if mine.owner != self.owner and mine.type == "Mine": 
#        if inRange(x,y,radius,mine.x,mine.y,mine.range):
#          for attacked in mine.allInRange(self.owner,mine.range):
#            attacked.health -= mine.damage
#            self.game.animations.append(['attack', mine.id, attacked.id])
#            if attacked.health <= 0 and attacked.id in self.game.objects:
#              self.game.removeObject(attacked)
#          self.game.removeObject(mine)
    return True

  def selfDestruct(self):
    if self.type == "Warp Gate":
      return "You cannot explode your Warp Gate"
    if self.owner != self.game.playerID:
      return "You can't make your opponenet's %s %i self destuct"%(self.type,self.id)
    for target in self.allInRange(self.owner^1, self.radius):   
      target.health -= self.selfDestructDamage
      if target.health <= 0 and target.id in self.game.objects:
        self.game.removeObject(target)
    self.game.removeObject(self)
    self.game.animations.append(['selfDestruct', self.id])
    return True
    
  def attack(self, target):
 #   if target.type == "Mine":
 #     return "You cannot attack mines"
    modifier = 1
    if self.owner != self.game.playerID:
       return "You cannot make your enemy's %s %i attack"%(self.type,self.id)
    if self.attacksLeft <= 0 or self.maxAttacks <=0:
      return "Your %s %i has no attacks left"%(self.type,self.id)
    if target.id in self.targeted and self.type == "Mine Layer":# and target.id == self.id:
      return "A mine layer can only lay one mine per turn"
      #return "This Mine Layer %i has already laid a mine this turn"(self.id)
    #if self.type == "Mine Layer" and target.id != self.id:
      #return "A Mine Layer lays a mine by attacking itself not %s %i"%(self.type,self.id)
    
    ######## MAY NOT NEED THIS, BUT MEH #############
    elif self.type == "Support":
      return "A support heals and buffs his comrades, he is not offensive"    
    if target.id in self.targeted:
      return "You have already commanded %s %i to attack %s %i"%(self.type,self.id,target.type,target.id)
    if self.type == "Mine Layer":
      #Adding a new mine to the game
      shipStats = [cfgUnits["Mine"][value] for value in self.game.ordering]   
      self.game.addObject(Ship, [self.game.playerID, self.x, self.y] + shipStats)
      self.maxAttacks-=1
      self.targeted.add(self.id)
      return True
    #Whenever the EMP attacks any target it will use an EMP
    if self.type == 'EMP': #and self.id == target.id:
      foe = self.owner^1
      for ship in self.allInRange(foe):
        ship.attacksLeft = -1
        ship.movementLeft = -1         
        self.maxAttacks -= 1
        self.game.animations.append(['attack',self.id,ship.id])
    elif target.owner == self.owner:
      return "No friendly fire. Your %s %i cannot attack your %s %i "%(self.type,self.id,target.type,target.id)
    elif not self.inRange(target):
      return "The target %s %i is too far away"%(target.type,target.id)
    else:
      #Factor in damage buff for Support ships neat opponent
      for unit in self.game.objects.ships:
        if unit.owner == self.owner:
          if unit.type == "Support":
            if unit.inRange(target):
            #Increment the damage modifier for each radar in range
              modifier+= (unit.damage / 100)
          
      self.game.animations.append(['attack', self.id, target.id])
      target.health-=self.damage*modifier
      self.attacksLeft -= 1
      if target.health <= 0 and target.id in self.game.objects:
        self.game.removeObject(target)
      self.targeted.add(target.id)
      if self.type == "Stealth":
        self.isStealthed = False
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
    if x**2 + y**2 > self.game.outerMapRadius**2:
      return "That ship would be lost in space...forever"
#    elif x**2 + y**2 < self.game.innerMapRadius**2:
#      return "Warping ships on the planet does not help in the fight!"
    elif player.energy < self.cost:
      return "You need to not be poor to buy that %s"%(self.type)
    elif not inRange(warpX,warpY,cfgUnits["Warp Gate"]["range"],x,y,0):
      return "You must spawn that %s closer to your Warp Gate"%(self.type)
    else:
      #spawn the unit with its stats, from units.cfg in config directory
      #Add unit to queue to be warped in at the beginning of this player's next turn
      self.game.objects.players[self.game.playerID].warping.append([self.type,x,y])
      player.energy -= self.cost
    return True
    


