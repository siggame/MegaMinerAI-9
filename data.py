# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Space"

globals = [ Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('round',int,'What round you are in the match'),
  Variable('victoriesNeeded', int,'How many victories a player needs to win'),
  Variable('mapRadius',int,'The radius of the map.  Center of screen is (0,0), with +x right, +y up')
]

constants = [
  ]
  
playerData = [
  Variable('victories',int,'How many rounds you have won this match'),
  Variable('energy', int, 'How much energy the player has left to warp in ships'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to display messages on the screen')
  ]

Ship = Model('Ship',
  data=[ Variable('owner', int, 'The owner of the piece'),
    Variable('x', int, 'Position x'),
    Variable('y', int, 'Position y'),
    Variable('radius', int, 'ship size radius'),
    Variable('type', str, 'The ship type'),
	  Variable('attacksLeft', int, 'how many more attacks it has'),
	  Variable('movementLeft', int, 'how much more movement it has'),
	  Variable('maxMovement', int, 'the largest possible movement'),
	  Variable('maxAttacks', int, 'the max number of attacks it has'),
	  Variable('damage', int, 'the strength of its attacks'),
	  Variable('range', int, 'the range of its attacks'),
	  Variable('health', int, 'the total health of the ship'),
	  Variable('maxHealth', int, 'the max health possible for the ship'),
	  Variable('selfDestructDamage', int, 'the amount of damage done when this ship blows up'),
    ],
  doc='A space ship!',
  functions=[ 
    Function('move', [Variable('x', int), Variable('y', int)], doc='Command a ship to move to a specified position'),
    Function ('selfDestruct', [], doc='Blow yourself up, damage those around you'),
  ],
)

Ship.addFunctions([Function("attack", [Variable("target", Ship)], doc='Commands your ship to attack a target')])

ShipType = Model('ShipType',
  data=[ Variable('type', str, 'The ship type'),
    Variable('cost', int, 'The amount of money required to purchase this type of ship'),
    ],
  functions=[Function('warpIn', [Variable('x', int), Variable('y', int)], doc='Sends in a new ship of this type'),
    ],
  doc='An available ship type',
  )

move = Animation('move',
  data=[ Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int),
    Variable('acting', Ship),
    ],
  )

attack = Animation('attack',
  data=[
    Variable('acting', Ship),
    Variable('target', Ship),
    ],
  )
  
selfDestruct = Animation ('selfDestruct' ,
  data=[
    Variable('acting', Ship),
    ],
  )

stealth = Animation('stealth',
  data=[
    Variable('acting', Ship),
    ],
  )

deStealth = Animation('deStealth',
  data=[
    Variable('acting', Ship),
    ],
  )
