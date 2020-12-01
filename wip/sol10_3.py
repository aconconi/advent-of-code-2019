from operator import itemgetter, attrgetter
from math import atan2, pi, hypot
# Position Object


class Pt(list):
    def __init__(self, x, y):
        self.value = y + x * 100
        self.x, self.y = x, y

    def __sub__(self, pt):
        return (pt.x - self.x, pt.y - self.y)

    def laser(self, n=200):
        ys = {k: v for k, _, v in self}
        return ys[sorted(ys)[n-1]]

    def refresh(self):
        for pt in Pt.Field:
            if pt is not self:
                offset = self - pt
                theta = atan2(*offset)
                yield (pi - theta, hypot(*offset), pt.value)

    def Identify(field):
        Pt.Field = (*field,)
        for pt in Pt.Field:
            pt += sorted(pt.refresh(), reverse=True)
            pt.targets = len({*map(itemgetter(0), pt)})
        return max(Pt.Field, key=attrgetter('targets'))


# Read Asteroid Grid
Station = Pt.Identify(Pt(x, y) for y, ln
                      in enumerate(open('../data/day10.dat'))
                      for x, o in enumerate(ln) if o == '#')
# Display Results
print("Silver:", Station.targets)
print("Gold:", Station.laser())
