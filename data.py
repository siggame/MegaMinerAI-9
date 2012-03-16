# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Space"

globals = [ Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('round',int,'The current round of the match'),
  Variable('victoriesNeeded', int,'How many victories a player needs to win'),
  Variable('innerMapRadius',int,'The inner radius of the map.  Center of screen is (0,0), with +x right, +y up'),
  Variable('outerMapRadius',int,'The outer radius of the map.  Center of screen is (0,0), with +x right, +y up'),
]

constants = [
  ]
  
playerData = [
  Variable('victories',int,'How many rounds you have won this match'),
  Variable('energy', int, 'How much energy the player has left to warp in ships'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to display messages on the screen'),
  ]

Ship = Model('Ship',
  data=[ Variable('owner', int, 'The owner of the ship'),
    Variable('x', int, 'X position of the ship'),
    Variable('y', int, 'Y position of the ship'),
    Variable('radius', int, 'The radius of the ship'),
    Variable('type', str, 'The ship type'),
	  Variable('attacksLeft', int, 'How many more attacks this ship has'),
	  Variable('movementLeft', int, 'How much more movement this ship has'),
	  Variable('maxMovement', int, 'The largest possible movement for this ship'),
	  Variable('maxAttacks', int, 'The max number of attacks for this ship'),
	  Variable('damage', int, 'The strength of attacks for this ship'),
	  Variable('range', int, 'The range of attacks for this ship'),
	  Variable('health', int, 'The total health of the ship'),
	  Variable('maxHealth', int, 'The max health possible for the ship'),
	  Variable('selfDestructDamage', int, 'The amount of damage done when this ship self destructs'),
    ],
  doc='A space ship!',
  functions=[ 
    Function('move', [Variable('x', int), Variable('y', int)], doc='Command a ship to move to a specified position. If the position specified by this function is not legal, the position of the ship will be updated, but the movement will be rejected by the server.'),
    Function ('selfDestruct', [], doc='Blow yourself up, damage those around you, reduces the ship to 0 health.'),
  ],
)

Ship.addFunctions([Function("attack", [Variable("target", Ship)], doc='Commands your ship to attack a target. Making an attack will reduce the number of attacks available to the ship, even if the attack is rejected by the game server.')])

ShipType = Model('ShipType',
  data=[ Variable('type', str, 'The ship type'),
    Variable('cost', int, 'The amount of money required to purchase this type of ship'),
    ],
  functions=[Function('warpIn', [Variable('x', int), Variable('y', int)], doc='Sends in a new ship of this type. Ships must be warped in with the radius of the player\'s warp ship.'),
    ],
  doc='An available ship type',
  )

move = Animation('move',
  data=[Variable('actingID', int),
    Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int),
    ],
  )

attack = Animation('attack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
    ],
  )
  
selfDestruct = Animation ('selfDestruct' ,
  data=[
    Variable('actingID', int),
    ],
  )

stealth = Animation('stealth',
  data=[
    Variable('actingID', int),
    ],
  )
  
#playerTalk = Animation('playerTalk',
  #data=[
    #Variable('actingID', int),
    #Variable('message', str),
    #],
  #)

deStealth = Animation('deStealth',
  data=[
    Variable('actingID', int),
    ],
  )
