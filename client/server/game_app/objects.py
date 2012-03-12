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

  def talk(self, message):
    pass



class Ship:
  def __init__(self, game, id, owner, x, y, radius, type, attacksLeft, movementLeft, maxMovement, maxAttacks, damage, range, health, maxHealth, selfDestructDamage, isStealthed, isEMPd):
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
    self.isStealthed = isStealthed
    self.isEMPd = isEMPd

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
      self.isStealthed,
      self.isEMPd,
      ]
    return value

  def nextTurn(self):
    pass

  def move(self, x, y):
    pass

  def selfDestruct(self):
    pass

  def attack(self, target):
    pass



