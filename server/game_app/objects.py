import math
def distance(fromX, toX, fromY, toY):
  return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))

def inRange(x1, y1, rad1, x2, y2, rad2):
  return distance(x1, x2, y1, y2) <= rad1 + rad2

class Player:
  def __init__(self, game, id, playerName, time, victories, money):
    self.game = game
    self.id = id
    self.playerName = playerName
    self.time = time
    self.victories = victories
    self.money = money

  def toList(self):
    value = [
      self.id,
      self.playerName,
      self.time,
      self.victories,
      self.money,
      ]
    return value

  def nextTurn(self):
    # If it's your turn and it isn't after the last turn, you get some energy
    if self.id == self.game.playerID:
      if self.game.turnNumber < self.game.turnLimit:
        self.energy += 50

  def talk(self, message):
    pass



class Ship:
  def __init__(self, game, id, owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, health, maxHealth):
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
    if x**2 + y**2 > self.game.mapRadius**2:
      return "Move is out of bounds of the map"
    else:
      moved = distance(self.x, x, self.y, y)
			#Checking to see if the ship hits a mine after moving 
			for unit in self.objects.ships:
			  if unit.owner != self.owner:
				  if unit.type == "mine":
				    if inRange(x,y,self.radius,unit.x,unit.y,unit.radius):	
						  #If a mine in range, hit the unit that moved there and destroy the mine
              self.health -= unit.damage						
						  self.game.removeObject(unit)
							if target.health <= 0:
                self.game.removeObject(self)
						  
      if self.movementLeft - moved < 0:
        return "Can not move that far"
      if moved == 0:
        return "Must move somewhere"
      self.game.animations.append(['move', self.x, self.y, x, y, self])
      self.x = x
      self.y = y
      self.movementLeft -= moved
      return True

  def selfDestruct(self):
    for target in self.objects.ships:
      if inRange (self.x, self.y, self.radius,target.x, target.y, target.radius):
        if target.owner != self.owner:
          #TODO placeholder value
          attack(target) 

  def attack(self, target):
    #Figure out how to get things from the config
    #if ConfigSectionMap("Fighter")['name'] == "fighter":
      #print ConfigSectionMap("Fighter")['name']
    if self.attacksLeft <= 0:
      return 'You have no attacks left'
		#TODO Make sure the type for mine layer matches up with the logic
		#Handles attacks for the mine layer
		#Minelayer attacks self to drop a mine at its center
    if self.type == "mineLayer" and self.id == target.id:
		  ##TODO Plug in data here for the "Mine" ship
		  self.game.addObject(Ship(owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, health, maxHealth))
			self.attacksLeft -= 1
		
    if target.owner == self.owner:
      return 'No friendly fire please'
    if not self.inRange (self, target):
      return "Target too far away"
    else:
		  modifier = 1
			#Checking to see if a radar is in range of the target
		  for unit in self.objects.ships:
			  if unit.owner == self.owner:
				  if unit.type == "radar":
				    if inRange(unit.x,unit.y,unit.range,target.x,target.y,target.radius):
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
    #TODO fill in ship values
	#TODO warp in ship range
	#TODO check player resources
    self.game.addObject(Ship,[owner, 
	  x, y, radius, type, attacksLeft, movementLeft, 
	  maxMovement, maxAttacks, damage, health, maxHealth
	  ])
	  
    


