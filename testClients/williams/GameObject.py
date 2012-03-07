# -*- python -*-

from library import library

from ExistentialError import ExistentialError

class GameObject(object):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration


##An available ship type
class ShipType(GameObject):
  def __init__(self, ptr):
    from BaseAI import BaseAI
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.shipTypeGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.shipTypes:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Sends in a new ship of this type
  def warpIn(self, x, y):
    self.validify()
    return library.shipTypeWarpIn(self.ptr, x, y)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.shipTypeGetId(self.ptr)

  ##The ship type
  def getType(self):
    self.validify()
    return library.shipTypeGetType(self.ptr)

  ##The amount of money required to purchase this type of ship
  def getCost(self):
    self.validify()
    return library.shipTypeGetCost(self.ptr)


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
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.playerGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.players:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Allows a player to display messages on the screen
  def talk(self, message):
    self.validify()
    return library.playerTalk(self.ptr, message)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.playerGetId(self.ptr)

  ##Player's Name
  def getPlayerName(self):
    self.validify()
    return library.playerGetPlayerName(self.ptr)

  ##Time remaining, updated at start of turn
  def getTime(self):
    self.validify()
    return library.playerGetTime(self.ptr)

  ##How many rounds you have won this match
  def getVictories(self):
    self.validify()
    return library.playerGetVictories(self.ptr)

  ##How much energy the player has left to warp in ships
  def getEnergy(self):
    self.validify()
    return library.playerGetEnergy(self.ptr)


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
    self.ptr = ptr
    self.iteration = BaseAI.iteration
    
    self.id = library.shipGetId(ptr)

  def validify(self):
    from BaseAI import BaseAI
    #if this class is pointing to an object from before the current turn it's probably
    #somewhere else in memory now
    if self.iteration == BaseAI.iteration:
      return True
    for i in BaseAI.ships:
      if i.id == self.id:
        self.ptr = i.ptr
        self.iteration = BaseAI.iteration
        return True
    raise ExistentialError()
  ##Command a ship to move to a specified position
  def move(self, x, y):
    self.validify()
    return library.shipMove(self.ptr, x, y)

  ##Blow yourself up, damage those around you
  def selfDestruct(self):
    self.validify()
    return library.shipSelfDestruct(self.ptr)

  ##Commands your ship to attack a target
  def attack(self, target):
    self.validify()
    if not isinstance(target, Ship):
      raise TypeError('target should be of [Ship]')
    target.validify()
    return library.shipAttack(self.ptr, target.ptr)

  ##Unique Identifier
  def getId(self):
    self.validify()
    return library.shipGetId(self.ptr)

  ##The owner of the piece
  def getOwner(self):
    self.validify()
    return library.shipGetOwner(self.ptr)

  ##Position x
  def getX(self):
    self.validify()
    return library.shipGetX(self.ptr)

  ##Position y
  def getY(self):
    self.validify()
    return library.shipGetY(self.ptr)

  ##ship size radius
  def getRadius(self):
    self.validify()
    return library.shipGetRadius(self.ptr)

  ##The ship type
  def getType(self):
    self.validify()
    return library.shipGetType(self.ptr)

  ##how many more attacks it has
  def getAttacksLeft(self):
    self.validify()
    return library.shipGetAttacksLeft(self.ptr)

  ##how much more movement it has
  def getMovementLeft(self):
    self.validify()
    return library.shipGetMovementLeft(self.ptr)

  ##the largest possible movement
  def getMaxMovement(self):
    self.validify()
    return library.shipGetMaxMovement(self.ptr)

  ##the max number of attacks it has
  def getMaxAttacks(self):
    self.validify()
    return library.shipGetMaxAttacks(self.ptr)

  ##the strength of its attacks
  def getDamage(self):
    self.validify()
    return library.shipGetDamage(self.ptr)

  ##the range of its attacks
  def getRange(self):
    self.validify()
    return library.shipGetRange(self.ptr)

  ##the total health of the ship
  def getHealth(self):
    self.validify()
    return library.shipGetHealth(self.ptr)

  ##the max health possible for the ship
  def getMaxHealth(self):
    self.validify()
    return library.shipGetMaxHealth(self.ptr)

  ##the amount of damage done when this ship blows up
  def getSelfDestructDamage(self):
    self.validify()
    return library.shipGetSelfDestructDamage(self.ptr)


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
