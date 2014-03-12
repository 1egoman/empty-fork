
# pygame
import pygame
from pygame.locals import *

# game objects
from gameobjects.vector2 import *

# math
from math import *

# random
import random

import inventory




class entity(object):


  def __init__(self, s, p, x, y):
    self.s = s
    self.parent = p

    self.x = x
    self.y = y

    self.w = 24
    self.h = 32

    sce = [(0,0), (28, 0), (28*3, 0), (28*4, 0)]
    f = self.img_list = self.slice_image( self.parent.src.entity_guy, sce)
    self.img = {"walk_w": f[2], "walk_e": None, "stationary": f[1]}

    self.pic = self.img["stationary"]


  # update entity
  def update(self):
    pass


  def render(self):
    # get information

    # bounding
    if self.x < 0: 
      self.x = 0
      self._vector = None

    if self.y < 0: 
      self.y = 0
      self._vector = None

    if self.x > self.parent.w: 
      self.x = self.parent.w-0.1
      self._vector = None

    if self.y > self.parent.h: 
      self.y = self.parent.h-0.1
      self._vector = None


    sx, sy = self.parent.to_screen(self.x, self.y)
    tx, ty = int(floor(self.x)), int(floor(self.y))
    h = self.parent.tiles[tx][ty].h-1

    # draw tile
    self.s.blit(self.pic, (sx-self.w/2, sy-self.h-self.parent.TILE_H/2*h))


  # get different sprite images from central image
  def slice_image(self, s, c):
    sp = []

    # loop through all positions
    for i,j in c:
      surf = pygame.Surface((self.w, self.h), SRCALPHA)
      surf.blit( s, (0, 0), (i, j, self.w, self.h) )
      sp.append(surf)

    return sp


  def click(self):
    # False will allow the click to not be 'used up' on the entity
    return False

  def delete(self):
    self.parent._entitys.remove(self)


# sandwich
class sandwich(entity):
  _MAX_ANTS = 10

  def render(self):
    self.w = 256
    self.h = 256

    # get center of map
    self.x = (self.parent.w/2)#(self.w/self.parent._TILE_W/2)
    self.y = (self.parent.h/2)#(self.h/self.parent._TILE_H/2)

    # draw sandwich
    sx, sy = self.parent.to_screen(self.x, self.y)

    # render
    self.s.blit( self.parent.src.sandwich, (sx, sy) )


  def click(self):
    # delete self
    self.delete()

    # spawn some ants
    for a in xrange(0, random.randint(1, self._MAX_ANTS)):
      # spawn an ant
      ax = self.x+random.randint(0, self.w*1.0/self.parent.TILE_W)
      ay = self.y+random.randint(0, self.h*1.0/self.parent.TILE_H)

      # spawn ants
      self.parent.spawn(ax, ay, ant)

    # notify user
    self.parent.notify.msg("Sandwich", "You finished up your sandwich, and found \nsome ants underneath!")
    return True




# fire
class fire(entity):
  _FIRE_CHANCE = 200

  def __init__(self, *args):
    super(fire, self).__init__(*args)
    self.CREATION_STAMP = self.parent.time
    self.w = self.parent._TILE_W
    self.h = self.parent._TILE_H*2

  def update(self): pass

  def render(self):

    for e in self.parent._entitys:
      if e.x > self.x and e.y < self.y and e.x < self.x+self.parent.TILE_W and e.y < self.y+self.parent.TILE_H:
        e.delete()

    # see if we turn it into bubble glass
    if random.randrange(0, self._FIRE_CHANCE) == 0:
      self.parent.tiles[self.x][self.y].tiles[-1] = inventory.items["bubbleglass"]

    # draw fire
    sx, sy = self.parent.to_screen(self.x, self.y)

    # render
    self.s.blit( self.parent.src.fire, (sx, sy-self.parent._TILE_H) )


  def click(self):
    # delete self
    self.delete()
    return True




# base mob class
class mob(entity):

  def __init__(self, s, p, x=None, y=None, *args):
    # check boundries
    if not x: x = round( random.uniform(0, p.w-1), 1)
    if not y: y = round( random.uniform(0, p.h-1), 1)

    # call super
    super(mob, self).__init__(s, p, x, y, *args)

    self._vector = None
    self._vector_orig_len = 0
    self._vector_orig_time = 0
    self._new_time = 0

    self._SPEED = self.parent.TILE_H/32 # in px a sec
    self._UPDATE_FREQUENCY = 0.1
    
    # test track

  def update(self):

    # display update
    if not self._vector: 
      self.pic = self.img['stationary']



    # movement update
    if self._new_time < self.parent.time: 

      # set new time
      self._new_time = self.parent.time+self._UPDATE_FREQUENCY


      # update movement (aimlessly wandering)
      if self._vector:


        # get screen coords
        sx, sy = self.parent.to_screen(self.x, self.y)

        # dt is the percentage of the way there we are
        dt = self.parent.time/(self._vector_orig_len/self._SPEED*self._UPDATE_FREQUENCY)

        # set length to new percentage
        self._vector.length = self._SPEED

        # increment our values
        self.x, self.y = self.parent.to_2d_tile(sx + self._vector[0], sy + self._vector[1], True)
        
        # check if we're done yet
        if self.x >= self._vector_end[0] and self.y >= self._vector_end[1]:
          self._vector = None


      else:
        # create a new vector
        x = round( random.uniform(0, self.parent.w-1), 1)
        y = round( random.uniform(0, self.parent.h-1), 1)

        # update image
        # if x <= self.x: 
        #   self.pic = self.img['walk_w']
        
        # if y <= self.y: 
        #   self.pic = self.img['walk_w']

        # go there
        self.track_to(x, y)


  # mob will go to point (x, y) @ self._SPEED
  def track_to(self, x, y):
    sx, sy = self.parent.to_screen(x, y)
    mx, my = self.parent.to_screen(self.x, self.y)

    # make sure we are going somewhere
    if (mx, my) == (sx, sy): return

    # update image
    # if sx <= mx: 
    #   self.pic = self.img['walk_w']
    #   print 1
    
    # if sy <= my: 
    #   self.pic = self.img['walk_w']
    #   print 2

    # create vector
    self._vector = Vector2.from_points( (mx, my), (sx, sy) )

    # get original length
    self._vector_orig_len = self._vector.length
    self._vector_orig_time = self.parent.time
    self._vector_total_time = self._vector_orig_len/self._SPEED
    self._vector_end = (x, y)


class ant(mob):
  pass