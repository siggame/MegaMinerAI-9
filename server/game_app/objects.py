import math
def distance(fromX, toX, fromY, toY):
   return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))

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
    pass

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
    pass

  def attack(self, target):
    pass



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
    pass



