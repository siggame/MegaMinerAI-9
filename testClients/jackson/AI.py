#-*-python-*-
from BaseAI import BaseAI
from GameObject import *
import math
import random

def distance(fromX, fromY, toX, toY):
  return int(math.ceil(math.sqrt((fromX-toX)**2 + (fromY-toY)**2)))

def grid_overlay(outer,inner,radial,spacing):
  radial_range = range(0,360,radial)
  spacing_range = range(inner,outer,spacing)
  points = []
  adj = dict()
  for d in radial_range:
    for r in spacing_range:
      x = r*math.cos(math.radians(d))
      y = r*math.sin(math.radians(d))
      points.append((int(x),int(y)))
  
  print "Generated %d points", len(points)

  #Now, we generate adjacencies:
  density = 16
  c = 0
  seen = set()
  
  shuf_p = points
  random.shuffle(shuf_p)

  for p1 in shuf_p:
    seen.add(p1)
    for p2 in shuf_p:
      if p2 in seen:
        continue
      d = distance(p1[0],p1[1],p2[0],p2[1])
      if d == 0:
        continue
      app = (d,p2[0],p2[1])
      try:
        #Expand the list
        if len(adj[p1]) >= density:
          if app < adj[p1][-1]:
            adj[p1].append(app)
        else:
          adj[p1].append(app)
        adj[p1].sort()
        adj[p1] = adj[p1][:density]
      except KeyError:
        #Start the list
        adj[p1] = [app]
      adj[p1] = adj[p1][:density] 
      app = (d,p1[0],p1[1])
      try:
        #Expand the list
        if len(adj[p2]) >= density:
          if app < adj[p2][-1]:
            adj[p2].append(app)
        else:
          adj[p2].append(app)
        adj[p2].sort()
        adj[p2] = adj[p2][:density]
      except KeyError:
        #Start the list
        adj[p2] = [app]
      adj[p2] = adj[p2][:density]
        

  for (k,v) in adj.iteritems():
    t = []
    for (d,x,y) in v:
      t.append((x,y,d))
    adj[k] = t
 
  print "Finished computing starfield... (beep boop)"  
 
  return (points,adj)

def simple_path(adj,start,goal):
  #First things first, we need to snap start to a point in our adj table
  start = min([ k for (k,v) in adj.iteritems() ],key=lambda x: distance(x[0],x[1],start[0],start[1]))
  #Next, we repeat the process for the goal point
  goal = min([ k for (k,v) in adj.iteritems() ],key=lambda x: distance(x[0],x[1],goal[0],goal[1]))
  print start
  print goal
  #Now we can follow a simple "reduce cost to zero" scheme
  current = start
  path = []
  k = 0
  while current[0] != goal[0] and current[1] != goal[1]:
    if k > 5000:
      print "Max path search!"
      break
    k += 1
    step = min( adj[(current[0],current[1])] ,key=lambda x: distance(x[0],x[1],goal[0],goal[1]))
    print "Picked %s distance remaining %s" % (step,distance(step[0],step[1],goal[0],goal[1]))
    path.append(step)
    current = step
  return path

class AI(BaseAI):
  """The class implementing gameplay logic."""
  @staticmethod
  def username():
    return "Battlestar"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    (self.points,self.adj) = grid_overlay(self.outerMapRadius(),self.innerMapRadius()+50,10,10)
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    #Setup stuff
    self.myships = [ x for x in self.ships if x.getOwner() == self.playerID() ]
    self.enemyships = [ x for x in self.ships if x.getOwner() != self.playerID() ]
    self.mygate = [ x for x in self.myships if x.getType() == "Warp Gate"][0]
    self.theirgate = [x for x in self.enemyships if x.getType() == "Warp Gate"][0]

    """
    for ship in self.ships:
        print "Ship %s at (%s,%s)" % (ship.getId(),ship.getX(),ship.getY())
    """

    #Buy cheap shit
    cheapest_ship = min(self.shipTypes, key=lambda x: x.getCost())
    for i in range(20):
      if self.players[self.playerID()].getEnergy() > cheapest_ship.getCost():
        cheapest_ship.warpIn(self.mygate.getX(), self.mygate.getY())

    for ship in self.myships:
      dest = random.choice(self.points)
      print "dest is %s,%s" % (dest)
      path = simple_path(self.adj,(ship.getX(),ship.getY()),dest)
      #print "path is %s" % (path)
      while len(path) > 0:
        (x,y,d) = path[0]
        path = path[1:]
        if d < ship.getMovementLeft():
          print "Trying to move from (%s,%s) to (%s,%s) I think it costs %s, game says > %s" % (ship.getX(),ship.getY(),x,y,d,ship.getMovementLeft())
          ship.move(x,y)
        else:
          break
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
