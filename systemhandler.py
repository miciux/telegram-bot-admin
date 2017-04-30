import logging
import abstracthandler
import os

class SystemHandler(abstracthandler.AbstractHandler):
  
  def __init__(self, conf, bot):
    abstracthandler.AbstractHandler.__init__(self, 'system', conf, bot)
    self.log = logging.getLogger(__name__)
    self.commands={}
    self.commands['cputemp'] = self.get_cpu_temp
    self.commands['uptime'] = self.get_uptime
    self.commands['pstree'] = self.get_pstree
    self.commands['reboot'] = self.reboot


  def handle_message(self,cid, command, args):
    try:
      self.commands[command](cid,args)
    except Exception as e:
      self.send_formatted_message(cid,self.get_sorry_message())
      self.log.error(e)

  def get_cpu_temp(self, cid, args):
    temp = open('/sys/class/thermal/thermal_zone0/temp','r').read()[0:-1]
    self.send_formatted_message(cid,'*%sC*'%temp)

  def execute_command(self, cid, command):
    result = os.popen(command).read()
    self.bot.sendMessage(cid, result)

  def get_uptime(self, cid, args):
    self.execute_command(cid, 'uptime')
 
  def get_pstree(self, cid, args):
    self.execute_command(cid, 'pstree')

  def reboot(self, cid, args):
    self.execute_command(cid, 'sudo reboot')

