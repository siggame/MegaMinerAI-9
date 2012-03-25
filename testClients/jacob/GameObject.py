# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration


##An available ship type
class ShipType(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.shipTypeGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.shipTypes:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Sends in a new ship of this type. Ships must be warped in with the radius of the player's warp ship.
  def warpIn(self, x, y):
    self.validify()
    return library.shipTypeWarpIn(self._ptr, x, y)

  #\cond
  def getId(self):
    self.validify()
    return library.shipTypeGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getType(self):
    self.validify()
    return library.shipTypeGetType(self._ptr)
  #\endcond
  ##The ship type
  type = property(getType)

  #\cond
  def getCost(self):
    self.validify()
    return library.shipTypeGetCost(self._ptr)
  #\endcond
  ##The amount of money required to purchase this type of ship
  cost = property(getCost)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "type: %s\n" % self.getType()
    ret += "cost: %s\n" % self.getCost()
    return ret

##
class Player(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.playerGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Allows a player to display messages on the screen
  def talk(self, message):
    self.validify()
    return library.playerTalk(self._ptr, message)

  #\cond
  def getId(self):
    self.validify()
    return library.playerGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self._ptr)
  #\endcond
  ##Player's Name
  playerName = property(getPlayerName)

  #\cond
  def getTime(self):
    self.validify()
    return library.playerGetTime(self._ptr)
  #\endcond
  ##Time remaining, updated at start of turn
  time = property(getTime)

  #\cond
  def getVictories(self):
    self.validify()
    return library.playerGetVictories(self._ptr)
  #\endcond
  ##How many rounds you have won this match
  victories = property(getVictories)

  #\cond
  def getEnergy(self):
    self.validify()
    return library.playerGetEnergy(self._ptr)
  #\endcond
  ##How much energy the player has left to warp in ships
  energy = property(getEnergy)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "playerName: %s\n" % self.getPlayerName()
    ret += "time: %s\n" % self.getTime()
    ret += "victories: %s\n" % self.getVictories()
    ret += "energy: %s\n" % self.getEnergy()
    return ret

##A space ship!
class Ship(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self._ptr = ptr
    self._iteration = BaseAI.iteration
    self._id = library.shipGetId(ptr)

  #\cond
  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self._iteration == BaseAI.iteration:
      return True
    for i in BaseAI.ships:
      if i._id == self._id:
        self._ptr = i._ptr
        self._iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  #\endcond
  ##Command a ship to move to a specified position. If the position specified by this function is not legal, the position of the ship will be updated, but the movement will be rejected by the server.
  def move(self, x, y):
    self.validify()
    return library.shipMove(self._ptr, x, y)

  ##Blow yourself up, damage those around you, reduces the ship to 0 health.
  def selfDestruct(self):
    self.validify()
    return library.shipSelfDestruct(self._ptr)

  ##Commands your ship to attack a target. Making an attack will reduce the number of attacks available to the ship, even if the attack is rejected by the game server.
  def attack(self, target):
    self.validify()
    if not isinstance(target, Ship):
      raise TypeError('target should be of [Ship]')
    target.validify()
    return library.shipAttack(self._ptr, target._ptr)

  #\cond
  def getId(self):
    self.validify()
    return library.shipGetId(self._ptr)
  #\endcond
  ##Unique Identifier
  id = property(getId)

  #\cond
  def getOwner(self):
    self.validify()
    return library.shipGetOwner(self._ptr)
  #\endcond
  ##The owner of the ship
  owner = property(getOwner)

  #\cond
  def getX(self):
    self.validify()
    return library.shipGetX(self._ptr)
  #\endcond
  ##X position of the ship
  x = property(getX)

  #\cond
  def getY(self):
    self.validify()
    return library.shipGetY(self._ptr)
  #\endcond
  ##Y position of the ship
  y = property(getY)

  #\cond
  def getRadius(self):
    self.validify()
    return library.shipGetRadius(self._ptr)
  #\endcond
  ##The radius of the ship
  radius = property(getRadius)

  #\cond
  def getType(self):
    self.validify()
    return library.shipGetType(self._ptr)
  #\endcond
  ##The ship type
  type = property(getType)

  #\cond
  def getAttacksLeft(self):
    self.validify()
    return library.shipGetAttacksLeft(self._ptr)
  #\endcond
  ##How many more attacks this ship has
  attacksLeft = property(getAttacksLeft)

  #\cond
  def getMovementLeft(self):
    self.validify()
    return library.shipGetMovementLeft(self._ptr)
  #\endcond
  ##How much more movement this ship has
  movementLeft = property(getMovementLeft)

  #\cond
  def getMaxMovement(self):
    self.validify()
    return library.shipGetMaxMovement(self._ptr)
  #\endcond
  ##The largest possible movement for this ship
  maxMovement = property(getMaxMovement)

  #\cond
  def getMaxAttacks(self):
    self.validify()
    return library.shipGetMaxAttacks(self._ptr)
  #\endcond
  ##The max number of attacks for this ship
  maxAttacks = property(getMaxAttacks)

  #\cond
  def getDamage(self):
    self.validify()
    return library.shipGetDamage(self._ptr)
  #\endcond
  ##The strength of attacks for this ship
  damage = property(getDamage)

  #\cond
  def getRange(self):
    self.validify()
    return library.shipGetRange(self._ptr)
  #\endcond
  ##The range of attacks for this ship
  range = property(getRange)

  #\cond
  def getHealth(self):
    self.validify()
    return library.shipGetHealth(self._ptr)
  #\endcond
  ##The total health of the ship
  health = property(getHealth)

  #\cond
  def getMaxHealth(self):
    self.validify()
    return library.shipGetMaxHealth(self._ptr)
  #\endcond
  ##The max health possible for the ship
  maxHealth = property(getMaxHealth)

  #\cond
  def getSelfDestructDamage(self):
    self.validify()
    return library.shipGetSelfDestructDamage(self._ptr)
  #\endcond
  ##The amount of damage done when this ship self destructs
  selfDestructDamage = property(getSelfDestructDamage)


  def __str__(self):
    self.validify()
    ret = ""
    ret += "id: %s\n" % self.getId()
    ret += "owner: %s\n" % self.getOwner()
    ret += "x: %s\n" % self.getX()
    ret += "y: %s\n" % self.getY()
    ret += "radius: %s\n" % self.getRadius()
    ret += "type: %s\n" % self.getType()
    ret += "attacksLeft: %s\n" % self.getAttacksLeft()
    ret += "movementLeft: %s\n" % self.getMovementLeft()
    ret += "maxMovement: %s\n" % self.getMaxMovement()
    ret += "maxAttacks: %s\n" % self.getMaxAttacks()
    ret += "damage: %s\n" % self.getDamage()
    ret += "range: %s\n" % self.getRange()
    ret += "health: %s\n" % self.getHealth()
    ret += "maxHealth: %s\n" % self.getMaxHealth()
    ret += "selfDestructDamage: %s\n" % self.getSelfDestructDamage()
    return ret
