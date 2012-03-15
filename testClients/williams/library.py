# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int, c_char_p]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
library.shipTypeWarpIn.restype = c_int
library.shipTypeWarpIn.argtypes = [c_void_p, c_int, c_int]

library.playerTalk.restype = c_int
library.playerTalk.argtypes = [c_void_p, c_char_p]

library.shipMove.restype = c_int
library.shipMove.argtypes = [c_void_p, c_int, c_int]

library.shipSelfDestruct.restype = c_int
library.shipSelfDestruct.argtypes = [c_void_p]

library.shipAttack.restype = c_int
library.shipAttack.argtypes = [c_void_p, c_void_p]

# accessors

#Globals 
library.getTurnNumber.restype = c_int
library.getTurnNumber.argtypes = [c_void_p]

library.getPlayerID.restype = c_int
library.getPlayerID.argtypes = [c_void_p]

library.getGameNumber.restype = c_int
library.getGameNumber.argtypes = [c_void_p]

library.getRound.restype = c_int
library.getRound.argtypes = [c_void_p]

library.getVictoriesNeeded.restype = c_int
library.getVictoriesNeeded.argtypes = [c_void_p]

library.getInnerMapRadius.restype = c_int
library.getInnerMapRadius.argtypes = [c_void_p]

library.getOuterMapRadius.restype = c_int
library.getOuterMapRadius.argtypes = [c_void_p]

library.getShipType.restype = c_void_p
library.getShipType.argtypes = [c_void_p, c_int]

library.getShipTypeCount.restype = c_int
library.getShipTypeCount.argtypes = [c_void_p]

library.getPlayer.restype = c_void_p
library.getPlayer.argtypes = [c_void_p, c_int]

library.getPlayerCount.restype = c_int
library.getPlayerCount.argtypes = [c_void_p]

library.getShip.restype = c_void_p
library.getShip.argtypes = [c_void_p, c_int]

library.getShipCount.restype = c_int
library.getShipCount.argtypes = [c_void_p]

# getters

#Data
library.shipTypeGetId.restype = c_int
library.shipTypeGetId.argtypes = [c_void_p]

library.shipTypeGetType.restype = c_char_p
library.shipTypeGetType.argtypes = [c_void_p]

library.shipTypeGetCost.restype = c_int
library.shipTypeGetCost.argtypes = [c_void_p]

library.playerGetId.restype = c_int
library.playerGetId.argtypes = [c_void_p]

library.playerGetPlayerName.restype = c_char_p
library.playerGetPlayerName.argtypes = [c_void_p]

library.playerGetTime.restype = c_float
library.playerGetTime.argtypes = [c_void_p]

library.playerGetVictories.restype = c_int
library.playerGetVictories.argtypes = [c_void_p]

library.playerGetEnergy.restype = c_int
library.playerGetEnergy.argtypes = [c_void_p]

library.shipGetId.restype = c_int
library.shipGetId.argtypes = [c_void_p]

library.shipGetOwner.restype = c_int
library.shipGetOwner.argtypes = [c_void_p]

library.shipGetX.restype = c_int
library.shipGetX.argtypes = [c_void_p]

library.shipGetY.restype = c_int
library.shipGetY.argtypes = [c_void_p]

library.shipGetRadius.restype = c_int
library.shipGetRadius.argtypes = [c_void_p]

library.shipGetType.restype = c_char_p
library.shipGetType.argtypes = [c_void_p]

library.shipGetAttacksLeft.restype = c_int
library.shipGetAttacksLeft.argtypes = [c_void_p]

library.shipGetMovementLeft.restype = c_int
library.shipGetMovementLeft.argtypes = [c_void_p]

library.shipGetMaxMovement.restype = c_int
library.shipGetMaxMovement.argtypes = [c_void_p]

library.shipGetMaxAttacks.restype = c_int
library.shipGetMaxAttacks.argtypes = [c_void_p]

library.shipGetDamage.restype = c_int
library.shipGetDamage.argtypes = [c_void_p]

library.shipGetRange.restype = c_int
library.shipGetRange.argtypes = [c_void_p]

library.shipGetHealth.restype = c_int
library.shipGetHealth.argtypes = [c_void_p]

library.shipGetMaxHealth.restype = c_int
library.shipGetMaxHealth.argtypes = [c_void_p]

library.shipGetSelfDestructDamage.restype = c_int
library.shipGetSelfDestructDamage.argtypes = [c_void_p]


#Properties
