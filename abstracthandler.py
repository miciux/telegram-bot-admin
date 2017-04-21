import emoji

class AbstractHandler():
  def __init__(self,
               name,
               conf, 
               bot):
    self.name = name
    self.config_data = conf
    self.bot = bot
    self.commands={}

  def handle_message(self, cid, command, args):
    raise NotImplementedError

  def handle_callback_query(self, qid, query_data):
    raise NotImplementedError    

  def get_sorry_message(self):
    command_list = '\n'.join(self.commands.keys())
    emojized = emoji.emojize('Questo non sembra un comando di *%s* :scream:\nEcco una lista dei comandi di *%s* disponibili:\n*%s*' , use_aliases=True)
    complete = emojized % (self.name, self.name, command_list)
    return complete

  def send_formatted_message(self, cid, message):
    self.bot.sendMessage(cid, message, parse_mode='Markdown')
