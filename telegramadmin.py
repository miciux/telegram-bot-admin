#!/usr/bin/env python

import sys
import logging
import time
import telepot
import json
import commandmanager

reload(sys).setdefaultencoding('utf-8')
logging.basicConfig(filename='telegramadmin.log')

class TelegramAdmin:

  def __init__(self):
    self.log = logging.getLogger('telegramadmin')
    self.config_data = {}
    self.bot = None
    self.command_list = None
    self.command_manager = None

  def main_loop(self):
    self.bot.message_loop({'chat': self.on_chat_message,
                      'callback_query': self.on_callback_query})
    self.log.info('Listening...')

    while 1:
      time.sleep(10)

  def on_chat_message(self, msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
      self.log.info('message received %s' % msg['text'])
      self.command_manager.execute_command_message(chat_id, msg['text'])

  def on_callback_query(self, msg):
    query_id, from_id, query_data = telepot.glance(msg,
                                                   flavour='callback_query')

  def init(self):
    with open('config.json') as json_config_file:
      self.config_data = json.load(json_config_file)

    TOKEN = self.config_data['token']

    self.bot = telepot.Bot(TOKEN)
 #   self.bot.sendMessage(self.config_data['uid'],"Ok, sono online!")

    self.command_manager = \
        commandmanager.CommandManager(self.bot, self.config_data)
    try:
      self.command_manager.load_handlers()
    except Exception as e:
      self.log.error(e)
      print 'Error importing modules, see logfiles for more infos'
      exit()

if __name__ == "__main__":
  server = TelegramAdmin()
  server.init()
  server.main_loop()

