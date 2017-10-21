import pygame
from pygame.locals import *

import entitys

# item dictionarys
items = {}
items_img = {}
items_args = {}


def create_item_dict(parent):
  # item width + height
  iw = 64

  # add items
  items["sand"] = 1
  items_img["sand"] = parent.src.sand
  items_args["sand"] = {
    "shape": "block", 
    "floats": False,
    "color": (217, 189, 167), 
    "item_img": pygame.transform.smoothscale(parent.src.item_sand, (iw,iw))
  }



  items["bubbleglass"] = 10
  items_img["bubbleglass"] = parent.src.bubbleglass
  items_args["bubbleglass"] = {
    "shape": "block", 
    "floats": True,
    "color": (100, 100, 100), 
    "item_img": pygame.transform.smoothscale(parent.src.bubbleglass, (iw,iw))
  }


  # just places an entity
  items["sandwich"] = 20
  items_img["sandwich"] = pygame.transform.smoothscale(parent.src.sandwich, (iw,iw))
  items_args["sandwich"] = {"shape": "flat", "place_entity": entitys.sandwich, "remove_on_place_entity": True}

  # just places an entity
  items["torch"] = 21
  items_img["torch"] = pygame.transform.smoothscale(parent.src.torch, (iw,iw))
  items_args["torch"] = {"shape": "flat", "place_entity": entitys.fire}



# "sand" -> 1
def get_name_from_id(id):
  for k,v in items.items():
    if v == id:
      return k

  return None


# main inventory object
class inv(object):

  def __init__(self, s, p):
    self.slots = []
    self.s = s
    self.parent = p

    self._INV_W = 9
    self._INV_H = 1
    self._INV_PADDING = 6
    self._INV_CELL_W = 64

    self.ACTIVE_CELL = (0, 0)

    self._FONT = pygame.font.Font(pygame.font.get_default_font(), 18)


  # get currently selected inventory item
  def get_selected_item(self):
    s_id = self.ACTIVE_CELL[1]*self._INV_W+self.ACTIVE_CELL[0]
    if s_id <= len(self.slots)-1:
      return self.slots[s_id]
    else:
      return None


  def render(self):

    # draw inventory bg
    self.w = self._INV_W*(self._INV_CELL_W+self._INV_PADDING)+self._INV_PADDING
    self.h = self._INV_H*(self._INV_CELL_W+self._INV_PADDING)+self._INV_PADDING
    self.x = (self.s.get_width()-self.w)/2
    self.y = (self.s.get_height()-self.h)
    pygame.draw.rect(self.s, (50, 50, 50, 0.5), (self.x, self.y, self.w, self.h))


    # draw inventory tiles
    for i in xrange(0, self._INV_W):
      for j in xrange(0, self._INV_H):
        tx = self.x + i*(self._INV_CELL_W+self._INV_PADDING)
        ty = self.y + j*(self._INV_CELL_W+self._INV_PADDING)


        # selected cell?
        if self.ACTIVE_CELL == (i,j):
          color = (120, 120, 120)
        else:
          color = (100, 100, 100)

        # render cell
        pygame.draw.rect(self.s, color, (self._INV_PADDING+tx, self._INV_PADDING+ty, self._INV_CELL_W, self._INV_CELL_W))

        # try to render any items within that cell
        s_id = j*self._INV_W+i
        if s_id > len(self.slots)-1: continue

        Iid = self.slots[s_id].id
        item_name = [k for k,v in items.items() if v == Iid]

        if item_name:
          our_item = self.slots[s_id]

          # split up any cells that need it (max stack size)
          while our_item.amt > our_item.MAX_AMT:
            self.slots.append( item(our_item.id, 1) )
            our_item.amt = our_item.MAX_AMT


          # render item picture
          if items_args[item_name[0]].has_key("item_img"):
            img = items_args[item_name[0]]["item_img"]
          else:
            img = items_img[item_name[0]]
          self.s.blit(img, (tx+6, ty+6))

          # also, render amount
          if our_item.amt > 1:
            rndr = self._FONT.render(str(our_item.amt), True, (255,255,255))
            self.s.blit(rndr, (tx+8, ty+8))




  def click(self, event): 
    # select different item
    mx, my = event.pos
    ix = (mx-self.x)/(self._INV_CELL_W+self._INV_PADDING)
    iy = (my-self.y)/(self._INV_CELL_W+self._INV_PADDING)

    self.ACTIVE_CELL = ix, iy


  # is item of type i in the inventory?
  def item_in_inventory(self, i):
    if isinstance(i, item):
      for c,d in enumerate(self.slots):
        if i.id == d.id:
          return c
      return False
    else:
      raise TypeError("value specified wasn't of type item")


  def room_in_inventory(self):
    if self._INV_W*self._INV_H <= len(self.slots) and self.slots[-1].amt == item.MAX_AMT: 
      return False
    else:
      return True


  # add item to inventory
  def add_item(self, i):

    # make sure there is romm in the inventory
    if not self.room_in_inventory(): return

    if isinstance(i, item):
      
      # if there is an item of this type already in the inventory
      d = self.item_in_inventory(i)
      if type(d) == int:
        # add the item
        self.slots[d] += i
      else:
        # otherwise add it to the inventory
        self.slots.append(i)

    else:
      raise TypeError("value specified wasn't of type item")


  # remove item to inventory
  def remove_item(self, i):
    if isinstance(i, item):
      
      # if there is an item of this type already in the inventory
      d = self.item_in_inventory(i)
      if type(d) == int:
        # remove the item
        self.slots[d] -= i
        if self.slots[d].amt <= 0: self.slots.remove( self.slots[d] )
      else:
        return False

    else:
      raise TypeError("value specified wasn't of type item")




# item object
class item(object):

  MAX_AMT = 16

  def __init__(self, id, amt=1):
    self.id = id
    self.amt = amt

  def __repr__(self):
    return "< ID: "+str(self.id)+", AMT: "+str(self.amt)+">"

  def __nonzero__(self):
    if self.amt:
      return True
    else:
      return False

  def __eq__(self, other):
    if isinstance(other, item) and self.id == other.id and self.amt == other.amt:
      return True
    else:
      return False 


  def __add__(self, other):
    return item(self.id, self.amt+other.amt)

  def __sub__(self, other):
    return item(self.id, self.amt-other.amt)

  def __mul__(self, other):
    return item(self.id, self.amt*other.amt)

  def __div__(self, other):
    return item(self.id, self.amt/other.amt)




  def __iadd__(self, other):
    self.amt += other.amt
    return self

  def __isub__(self, other):
    self.amt -= other.amt
    return self

  def __imul__(self, other):
    self.amt *= other.amt
    return self

  def __idiv__(self, other):
    self.amt /= other.amt
    return self
