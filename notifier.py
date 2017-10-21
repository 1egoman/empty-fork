import pygame

# notification class
class notifier(object):

  def __init__(self, p, s):
    self.lst = []
    self.s = s
    self.parent = p
    self._FONT_HEAD = pygame.font.Font(pygame.font.get_default_font(), 24)
    self._FONT = pygame.font.Font(pygame.font.get_default_font(), 18)
    self._MARGINS = 20
    self._DISP_TIME = 3


  # send user a message
  def msg(self, t="Information", m="Hello, World!"):
    self.lst = [t, m]
    self.parent.flush_events("notification_dissmissed")

    # schedule deletion
    self.parent.schedule_time(self.parent.time+self._DISP_TIME, self.destruct, [len(self.lst)-1], "notification_dissmissed")

  # render notification
  def render(self):

    # draw last notification
    if not len(self.lst): return 

    # render dialog
    d = self.parent.src.info_msg
    dx = self.s.get_width()-d.get_width()
    self.s.blit( d, (dx, 0) )

    # title
    rndr1 = self._FONT_HEAD.render(self.lst[0], True, (255,255,255))
    self.s.blit( rndr1, (dx+self._MARGINS, self._MARGINS) )

    # body message (split on \n to form lines)
    s = self.lst[1].split("\n")
    for c,d in enumerate(s):
      rndr2 = self._FONT.render(d, True, (255,255,255))
      self.s.blit( rndr2, (dx+self._MARGINS, self._MARGINS*1.25+rndr1.get_height()+c*rndr2.get_height()) )


  # remove notification # d
  def destruct(self, d):
    self.lst = []
