import logging
import abstracthandler
import datetime

class DefaultHandler(abstracthandler.AbstractHandler):

    def __init__(self, conf, bot):
        abstracthandler.AbstractHandler.__init__(self, 'default', conf, bot)
        self.log = logging.getLogger(__name__)
        self.commands={}
        self.commands['time'] = self.get_time
        self.commands['log'] = self.get_log

    def handle_message(self,cid, command, args):
        try:
            self.commands[command](cid,args)
        except Exception as e:
            self.send_formatted_message(cid,self.get_sorry_message())
            self.log.error(e)

    def get_time(self, cid, args):
        self.bot.sendMessage(cid, str(datetime.datetime.now()))

    def get_log(self, cid, args):
        self.bot.sendMessage(cid, open('telegramadmin.log','r').read())
