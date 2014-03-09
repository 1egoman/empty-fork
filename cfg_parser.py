import cPickle as pickle
# import pickle
import tiles


def parse(data):

  # turn tile into a transport tile (used for storage)

  # duplicate map
  m = [x[:] for x in data['map']]

  # parse it
  for x in xrange(data['width']-1, -1, -1):
    for y in xrange(0, data['height']):
      m[x][y] = tile_trans(m[x][y])


  data['map'] = m


  # return it, pickled
  return pickle.dumps(data, -1)



# load map data
def load(world, s, data):

  data = pickle.loads(data)
  dmap = []

  for x in xrange(data['width']-1, -1, -1):
    dmap.append([])

    for y in xrange(0, data['height']):
      dmap[-1].append( data['map'][x][y].unpack(world, s) )


  data['map'] = dmap


  return data



# used to store a tile's values
class tile_trans(object):

  def __init__(self, tile):
    self.__dict__ = tile.__dict__.copy()
    self._TYPE = tile.__class__.__name__

    # delete problems
    self.BLOCK = []
    del self.parent

  def unpack(self, world, s):
    # repack the temp storage into an actual tile

    # what tile we need to create
    i = getattr(tiles, self._TYPE)
    n = i(world, self.x, self.y, self.color, self.s)
    n.__dict__ = self.__dict__.copy()
    n.parent = world
    n.s = s
    return n
