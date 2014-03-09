# pygame
import pygame
from pygame.locals import *

# os
import os

# my files
import world
import main_menu


class app(object):

  BG_COLOR = (180, 180, 180)

  def __init__(self):

    # init vars
    self.w = 800
    self.h = 500
    self.running = True


    # init pygame
    pygame.init()


    # create screen
    self.s = pygame.display.set_mode((self.w, self.h), RESIZABLE)
    pygame.display.set_caption("The Sandbox-Sandbox DEV0.1")


    # go to menu
    self.s, w = main_menu.go(self.s)
    if not w: return


    # create clock
    self.clock = pygame.time.Clock()


    # create map, load world, and center it
    self.wld = world.map(self.s, w=16, h=16)

    # load map if possible
    if os.listdir(os.path.join("saves", w)) != []: 
      self.wld.load_map(w)
    else:
      # create a new map, and save it
      self.wld.save_map(w, notify=False)

    self.wld.center_map((self.w,self.h))


    # loop
    self.loop()


  def loop(self):

    # set mouse invisible
    # pygame.mouse.set_visible(False)

    while self.running:
      
      # tick clock
      self.clock.tick()
      self.wld.FPS = self.clock.get_fps()

      # events
      for event in pygame.event.get():

        if event.type == QUIT:
          # quit program
          self.running = False
          return

        elif event.type == VIDEORESIZE:
          # resize screen
          self.w, self.h = event.size
          self.s = pygame.display.set_mode((self.w, self.h), RESIZABLE)

          # center map on screen
          self.wld.center_map(event.size)


        elif event.type == KEYDOWN:
          if event.unicode == "w": self.wld.yo += self.wld.TILE_H
          if event.unicode == "s": self.wld.yo -= self.wld.TILE_H
          if event.unicode == "d": self.wld.xo -= self.wld.TILE_W
          if event.unicode == "a": self.wld.xo += self.wld.TILE_W

          # save/load
          if event.unicode == "q": self.wld.save_map()
          if event.unicode == "e": self.wld.load_map(self.wld._NAME)

          # test notification
          if event.key == K_ESCAPE:

            print self.wld.clock
            self.wld.clock.pause()

            # go (back) to menu
            self.s, w = main_menu.go(self.s)
            if not w: return

            # load map if possible
            if os.listdir(os.path.join("saves", w)) != []: 
              self.wld.load_map(w)
            else:
              # create a new map, and save it
              self.wld.flush_map()
              self.wld.save_map(w, notify=False)

            self.wld.center_map((self.w,self.h))

            # uppause clock
            self.wld.clock.unpause()


          # debug (F1)
          if event.key == 282: 
            self.wld._DIAGNOSTIC = not self.wld._DIAGNOSTIC
            if self.wld._DIAGNOSTIC: self.wld.notify.msg("Diagnostics", "Diagnostics mode has been enabled.")


        elif event.type == MOUSEMOTION:
          # send mouse motion
          self.wld.send_motion( event )

        elif event.type == MOUSEBUTTONDOWN:
          # send mouse motion
          self.wld.send_mousebutton( event, "down" )

        elif event.type == MOUSEBUTTONUP:
          # send mouse motion
          self.wld.send_mousebutton( event, "up" )



      # draw background
      self.s.fill(self.wld.BG_COLOR)

      # render world
      self.wld.render()

      # flip screen
      pygame.display.flip()


    # make mouse visible again
    pygame.mouse.set_visible(True)


if __name__ == '__main__':
  a = app()

