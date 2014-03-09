import pygame
from pygame.locals import *

import os
import shutil


# MAIN MENU
def go(s):

  logo_h = 200

  # load images
  logo = pygame.image.load( os.path.join("src", "menu", "logo.png") ).convert_alpha()

  button = pygame.image.load( os.path.join("src", "menu", "button.png") ).convert_alpha()

  play_button = pygame.image.load( os.path.join("src", "menu", "playbutton.png") ).convert_alpha()
  play_button_down = pygame.image.load( os.path.join("src", "menu", "playbuttondown.png") ).convert_alpha()
  play_down = False

  loop = 1
  while loop:

    cx = (s.get_width() - play_button.get_width())/2

    # events
    for event in pygame.event.get():



      if event.type == QUIT:
        # quit program
        return s, None



      elif event.type == VIDEORESIZE:
        # resize screen
        s = pygame.display.set_mode(event.size, RESIZABLE)



      elif event.type == MOUSEBUTTONDOWN:
        mx, my = event.pos

        # play button
        if mx >= cx and mx <= cx+play_button.get_width() and my >= logo_h+64 and my <= logo_h+play_button.get_height()+64:
          play_down = True
          # return s, "world"
        else:
          play_down = False




      elif event.type == MOUSEBUTTONUP:
        mx, my = event.pos

        # play button
        if mx >= cx and mx <= cx+play_button.get_width() and my >= logo_h+64 and my <= logo_h+play_button.get_height()+64:
          a = load_new_world(s)
          print a
          if a: return a
        
        play_down = False


    # fill screen
    s.fill((180,180,180))

    # draw buttons and logo
    s.blit(logo, (cx, 16 ))

    if play_down:
      s.blit(play_button_down, (cx, logo_h+64))
    else:
      s.blit(play_button, (cx, logo_h+64))

    s.blit(button, (cx, logo_h+play_button.get_height()+80 ))

    # flip
    pygame.display.flip()






# WORLD SELECTION
def load_new_world(s):


  new_button = pygame.image.load( os.path.join("src", "menu", "newbutton.png") ).convert_alpha()
  del_button = pygame.image.load( os.path.join("src", "menu", "delbutton.png") ).convert_alpha()
  back_button = pygame.image.load( os.path.join("src", "menu", "backbutton.png") ).convert_alpha()
  go_button = pygame.image.load( os.path.join("src", "menu", "gobutton.png") ).convert_alpha()

  new_button_down = pygame.image.load( os.path.join("src", "menu", "newbuttondown.png") ).convert_alpha()
  del_button_down = pygame.image.load( os.path.join("src", "menu", "delbuttondown.png") ).convert_alpha()
  back_button_down = pygame.image.load( os.path.join("src", "menu", "backbuttondown.png") ).convert_alpha()
  go_button_down = pygame.image.load( os.path.join("src", "menu", "gobuttondown.png") ).convert_alpha()

  slider = pygame.image.load( os.path.join("src", "menu", "slider.png") ).convert_alpha()

  font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
  iH = 96 # each list item's height
  selected = None
  sP = 0.0
  scroll = False

  new_down = del_down = back_down = go_down = False
  loop = 1
  while loop:

    W = 512
    H = 256
    cx = (s.get_width() - W)/2


    if s.get_height() > 512+96:
      H = 512
    else:
      H = 256


    # events
    for event in pygame.event.get():



      if event.type == QUIT:
        # quit program
        return s, None



      elif event.type == VIDEORESIZE:
        # resize screen
        s = pygame.display.set_mode(event.size, RESIZABLE)



      elif event.type == MOUSEMOTION:
        mx, my = event.pos

        m = pygame.mouse.get_pressed()

        # selectbox
        my -= 16
        if scroll and m[0] and my <= H+16 and mx > cx+W+8 and mx < cx+W+40:
            # adjust scrollbar
            sP = my*1.0/H
            if sP < 0: sP = 0
            if sP > 1: sP = 1.0


      elif event.type == MOUSEBUTTONDOWN:
        mx, my = event.pos


        if scroll and event.button == 5: sP += 0.05
        if scroll and event.button == 4: sP -= 0.05
        if sP < 0: sP = 0
        if sP > 1: sP = 1.0



        # selectbox
        if event.button == 1 and my <= H+16:
          my -= 16
          if scroll and mx > cx+W+8 and mx < cx+W+40:
            # adjust scrollbar
            sP = my-16*1.0/H
            if sP < 0: sP = 0
            if sP > 1: sP = 1.0
          else:
            my += mD
            selected = my/iH


        # new
        if mx > cx and mx < cx+new_button.get_width() and my > 32+H and my < 32+H+new_button.get_height():
          new_down = True
        else:
          new_down = False

        # delete
        if selected != None and mx > W-new_button.get_width()+cx and mx < W+cx and my > 32+H and my < 32+H+new_button.get_height():
          del_down = True
        else:
          del_down = False

        # go (cx+new_button.get_width()+10, 32+H )
        if selected != None and mx > cx+new_button.get_width()+10 and mx < cx+new_button.get_width()+10+go_button.get_width() and my > 32+H and my < 32+H+new_button.get_height():
          go_down = True
        else:
          go_down = False

        # back
        if mx > cx and mx < cx+new_button.get_width() and my > 42+new_button.get_height()+H and my < 42+new_button.get_height()+H+back_button.get_height():
          back_down = True
        else:
          back_down = False


      elif event.type == MOUSEBUTTONUP:
        mx, my = event.pos

        # add
        if mx > cx and mx < cx+new_button.get_width() and my > 32+H and my < 32+H+new_button.get_height():
          return new_world(s)

        # delete
        if selected != None and mx > W-new_button.get_width()+cx and mx < W+cx and my > 32+H and my < 32+H+new_button.get_height():
          # delete world
          shutil.rmtree( os.path.join("saves", worlds[selected]) )
          

        # back
        if mx > cx and mx < cx+new_button.get_width() and my > 42+new_button.get_height()+H and my < 42+new_button.get_height()+H+back_button.get_height():
          return None

        if selected != None and mx > cx+new_button.get_width()+10 and mx < cx+new_button.get_width()+10+go_button.get_width() and my > 32+H and my < 32+H+new_button.get_height():
          # launch selected World
          return s, worlds[selected]
        
        # deselect buttons
        new_down = False
        del_down = False
        back_down = False
        go_down = False

        if my > H+16 and mx < cx or mx > cx+H: selected = None


    # fill screen
    s.fill((180,180,180))


    # draw selectbox
    worlds = os.listdir("saves")

    pygame.draw.rect(s, (100, 100, 100), (0, 16, s.get_width(), H))
    pygame.draw.rect(s, (0, 0, 0), (-10, 16, s.get_width()+20, H), 3)
    

    if scroll: pygame.draw.rect(s, (140, 140, 140), (cx+W+8, 18, 32, H-4))

    tH = iH*(len(worlds))
    if scroll: s.blit(slider, ( cx+W+12, 18+((H-46)*sP)+4 ))
    if sP < 0: sP = 0.0
    if sP > 1: sP = 1.0
    mD = int( (tH-H+iH)*sP )
    if selected > len(worlds)-1 or selected < 0: 
      selected = None


    # draw selectbox contents
    aa = False
    for c,e in enumerate(worlds):

      # stop when list reaches capacity
      if iH*(c+1)+20-mD > H+16: 
        scroll = True
        aa = True
        break

      # draw selection
      if selected == c:

        d = iH

        pygame.draw.rect(s, (120, 120, 120), (cx, c*iH+20-mD, W, d))

      # render item
      rndr = font.render(e, 1, (255,255,255))
      s.blit(rndr, (cx+20, c*iH+32-mD))


    # update scroll
    if not aa and mD < 0: scroll = False



    # draw buttons
    if new_down:
      s.blit(new_button_down, (cx, 32+H ))
    else:
      s.blit(new_button, (cx, 32+H ))


    if back_down:
      s.blit(back_button_down, (cx , 42+new_button.get_height()+H))
    else:
      s.blit(back_button, (cx , 42+new_button.get_height()+H))



    if selected != None:
      if del_down:
        s.blit(del_button_down, (W-new_button.get_width()+cx , 32+H))
      else:
        s.blit(del_button, (W-new_button.get_width()+cx , 32+H))



      if go_down:
        s.blit(go_button_down, (cx+new_button.get_width()+10, 32+H ))
      else:
        s.blit(go_button, (cx+new_button.get_width()+10, 32+H ))


    # flip
    pygame.display.flip()





def new_world(s):

  go_button = pygame.image.load( os.path.join("src", "menu", "gobutton.png") ).convert_alpha()
  go_button_down = pygame.image.load( os.path.join("src", "menu", "gobuttondown.png") ).convert_alpha()
  go_down = False

  font = pygame.font.SysFont(pygame.font.get_default_font(), 48)
  name = ""

  while 1:

    cx = (s.get_width() - go_button.get_width())/2

    # events
    for event in pygame.event.get():



      if event.type == QUIT:
        # quit program
        return s, None



      elif event.type == VIDEORESIZE:
        # resize screen
        s = pygame.display.set_mode(event.size, RESIZABLE)


      elif event.type == KEYDOWN:
        if event.key == K_BACKSPACE:
          name = name[:-1]
        else:
          name += event.unicode



      elif event.type == MOUSEBUTTONDOWN:
        mx, my = event.pos

        # go button
        if name and mx >= cx and mx <= cx+go_button.get_width() and my >= 200 and my <= go_button.get_height()+200:
          go_down = True
        else:
          go_down = False




      elif event.type == MOUSEBUTTONUP:
        mx, my = event.pos

        # go  button
        if name and mx >= cx and mx <= cx+go_button.get_width() and my >= 200 and my <= go_button.get_height()+200:
          
          # make world dir
          p = os.path.join("saves", name)
          if not os.path.exists(p): os.mkdir(p)
          
          return s, name
        
        go_down = False


    # fill screen
    s.fill((180,180,180))

    rndr = font.render("World Name: ", 1, (255,255,255))
    s.blit(rndr, (cx, 48))

    pygame.draw.rect(s, (120,120,120), (cx, 96, 512, 64))
    rndr = font.render(name, 1, (255,255,255))
    s.blit(rndr, (cx+10, 110))

    if name and go_down:
      s.blit(go_button_down, (cx, 200))
    elif name:
      s.blit(go_button, (cx, 200))

    # flip
    pygame.display.flip()