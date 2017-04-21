import logging
import abstracthandler
import os

class FileHandler(abstracthandler.AbstractHandler):
  
  def __init__(self, conf, bot):
    abstracthandler.AbstractHandler.__init__(self, 'file', conf, bot)
    self.log = logging.getLogger(__name__)
    self.commands={}
    self.commands['list'] = self.get_file_list

  def handle_message(self,cid, command, args):
    try:
      self.commands[command](cid,args)
    except Exception as e:
      self.send_formatted_message(cid,self.get_sorry_message())
      self.log.error(e)

  def get_file_list(self, cid, args):
    if len(args) >= 1:
      for folder in args:
        self.send_formatted_message(cid,self.get_folder_content(folder))
    else:
      self.send_formatted_message(cid,'*file list* usage: file list _[DIRECTORY]_...')

  def get_folder_content(self, folder):
    message = 'Lista dei files in *%s*:\n_%s_'
    files = '\n'.join(os.listdir(folder))
    return message % (folder,files);

