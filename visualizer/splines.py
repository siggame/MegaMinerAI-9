from numpy import array, dot
import pylab

A = array([
  [1, 0, -3, 2],
  [0, 1, -2, 1],
  [0, 0, 3, -2],
  [0, 0, -1, 1]]).transpose()


def spline(t, m0, p0, p1, m1):
  times = array([1, t, t ** 2, t ** 3])

  q = array([p0, m0, p1, m1])
  m = dot(dot(times, A), q)

  return m

m0 = array([0, 0])
p0 = array([0, 10])
p1 = array([50, 10])
m1 = array([50, 0])

xs = []
ys = []

for i in xrange(0, 101, 1):
  t = i / 100.0
  s = spline(t, p0 - m0, p0, p1, m1 - p1)
  xs.append(s[0])
  ys.append(s[1])

pylab.plot(xs, ys)
pylab.show()
