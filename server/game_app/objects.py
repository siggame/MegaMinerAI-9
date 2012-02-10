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
    pass

  def move(self, x, y):
    pass

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



