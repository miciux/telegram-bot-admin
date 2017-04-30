import importlib
import emoji
import logging

sorry_message=emoji.emojize(u'Perdonami ma non riconosco questo tipo di richiesta. :sob:\nMagari quando hai tempo insegnami come gestirla :wink:', use_aliases=True)


class CommandManager():
  def  __init__(self, bot, conf):
    self.bot = bot
    self.config_data = conf
    self.handlers = None
    self.log = logging.getLogger(__name__)

  def load_handlers(self):
    plugins_to_import = self.config_data['plugins']

    plugins_objects = [getattr(importlib.import_module(mod),cls)(self.config_data, self.bot)
                for (mod,cls) in (plugin.split('.')
                  for plugin in plugins_to_import.values())]
    self.handlers = dict(zip(plugins_to_import.keys(),plugins_objects))

  def parse_command_message(self, command_text):
    parsed_command = {}
    parsed_command['type'] = ''
    parsed_command['name'] = ''
    parsed_command['args'] = []
    split_command = command_text.split()

    if len(split_command) > 0:
      parsed_command['type'] = split_command[0]
    if len(split_command) > 1:
      parsed_command['name'] = split_command[1]
    else:
      parsed_command['type'] = 'default'
      parsed_command['name'] = split_command[0]
    if len(split_command) > 2:
      parsed_command['args'] = split_command[2:]

    return parsed_command

  def execute_command_message(self, cid, command):
    parsed_command = self.parse_command_message(command)
    command_handlers = None

    try:
      command_handler = self.handlers[parsed_command['type']]
    except Exception as e:
      self.log.error(e)
      self.bot.sendMessage(cid, sorry_message)
      return

    command_handler.handle_message(cid,
                             parsed_command['name'],
                             parsed_command['args'])
