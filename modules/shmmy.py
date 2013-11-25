# -*- coding: utf-8 -*-
## Extension module for shmmy IRC needs

## Created By    : Vasilis Gerakaris <vgerak@gmail.com>
## Last Revision : 25-11-2013

from time import strftime

class Shmmy(object):
  def __init__(self, bot):
    self.bot = bot
    self.plaisia = {}
    self.speaker = ""
    self.speakerTime = ""
    self.attendance = ""
    self.attendanceTime = ""

    self.commands = {               # Module Commands
      "omilitis" : self.omilitis,
      "omilitis_" : self.setOmilitis,
      "clearOmilitis_" : self.clearOmilitis,
      "apartia" : self.apartia,
      "apartia_" : self.setApartia,
      "plaisia" : self.plaisia,
      "plaisia_" : self.plaisia,
      "order_" : self.order,
      "count_" : self.count,
      "results" : self.results,
      "results_" : self.results,
      "help" : self.help,
      "help_" : self.help,
    }

    self.counter = {}

  def decode(self, user, cmd, args):
    command = self.demux(cmd)
    try:
      if user in self.bot.copyuser:
        self.commands[command + "_"](user, args)
      else:
        self.commands[command](user)
    except KeyError:
      self.error(user)
    except Exception, e:
      print e

  def demux(self, cmd):
    if cmd in ["ομιλιτης", "ομιλιτής", "speaker", "omilitis"]:
      return "omilitis"
    elif cmd in ["πλαισια", "πλαίσια", "plaisia"]:
      return "plaisia"
    elif cmd in ["απαρτια", "απαρτία", "apartia"]:
      return "apartia"
    elif cmd in ["αποτελεσματα", "αποτελέσματα", "results", "apotelesmata"]:
      return "results"
    else:
      return cmd

  def omilitis(self, nick):
    if self.speaker:
      self.bot.s.send("PRIVMSG {0} : Τρέχων ομιλιτής: {1}, Τελευταία ενημέρωση: {2} \r\n".format(nick,self.speaker,self.speakerTime))
    else:
      self.bot.s.send("PRIVMSG {0} : Δεν έχει οριστεί ομιλιτής. \r\n".format(nick))

  def setOmilitis(self, nick, args):
    if args:
      self.speakerHistory.append((self.speaker,self.speakerTime))
      self.speaker = " ".join(args)
      self.speakerTime = strftime('%H:%M')
      self.bot.s.send("PRIVMSG {0} : Τρέχων ομιλιτής: {1}, Τελευταία ενημέρωση: {2} \r\n".format(nick,self.speaker,self.speakerTime))
    else:
      self.omilitis(nick)

  def clearOmilitis(self, nick, args):
    self.omilitis = ""
    self.bot.s.send("PRIVMSG {0} : Δεν έχει οριστεί ομιλιτής. \r\n".format(nick))

  def apartia(self, nick):
    if self.attendance:
      self.bot.s.send("PRIVMSG {0} : Εκτιμώμενη απαρτία: {1}, Τελευταία ενημέρωση: {2} \r\n".format(nick,self.attendance,self.attendanceTime))
    else:
      self.bot.s.send("PRIVMSG {0} : Δεν έχει δοθεί εκτίμηση για απαρτία. \r\n".format(nick))

  def setApartia(self, nick, args):
    if args:
      self.attendance = args[0]
      self.attendanceTime = strftime('%H:%M')
      self.bot.s.send("PRIVMSG {0} : Εκτιμώμενη απαρτία: {1}, Τελευταία ενημέρωση: {2} \r\n".format(nick,self.attendance,self.attendanceTime))
    else:
      self.apartia(nick)

  def plaisia(self, nick, args=[]):
    self.bot.s.send("PRIVMSG {0} : Βαριόμουν να τα υλοποιήσω. Να ήσουν στη ΓΣ να τα άκουγες! :) \r\n".format(nick))

  def order(self, nick, args):
    if args:
      for i in args:
        self.counter[i] = 0

  def results(self, nick, args=[]):
    if self.counter:
      print "Τρέχοντα αποτελέσματα"
      self.bot.s.send("PRIVMSG {0} : Τρέχοντα αποτελέσματα\r\n".format(nick))
      for i in self.counter:
        print "{0:4} : {1}".format(self.counter[i], i)
        self.bot.s.send("PRIVMSG {0} : {1:4} : {2}\r\n".format(nick, self.counter[i], i))

  def count(self, nick, args):
    if args:
      self.lastCount = args
      for i, val in enumerate(self.counter):
        self.counter[val] += int(args[i])
      self.results(self.bot.HOME_CHANNEL)

  def help(self, nick, args=[]):
    self.bot.s.send("PRIVMSG {0} : Διαθέσιμες εντολές: .plaisia, .omilitis, .apartia, .apotelesmata, .plaisia \r\n".format(nick))
    if nick in self.bot.copyuser:
      self.bot.s.send("PRIVMSG {0} : Επιπλέον εντολές: .clearOmilitis, .order, .count \r\n".format(nick))

  def error(self, nick, args=[]):
    self.bot.s.send("PRIVMSG {0} : Η εντολή δεν υπάρχει. \r\n".format(nick))
    self.help(nick)