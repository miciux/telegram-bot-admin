import logging
import abstracthandler
import transmissionrpc
import os

class TorrentHandler(abstracthandler.AbstractHandler):
  
  def __init__(self, conf, bot):
    abstracthandler.AbstractHandler.__init__(self, 'torrent', conf, bot)
    self.log = logging.getLogger(__name__)
    self.tc = None
    self.commands={}
    self.commands['list'] = self.get_torrent_list
    self.commands['info'] = self.get_torrent_info
    self.commands['add'] = self.add_torrent
    self.commands['remove'] = self.remove_torrent
    self.commands['stop'] = self.stop_torrent
    self.commands['start'] = self.start_torrent
    self.commands['stopall'] = self.stop_all
    self.commands['startall'] = self.start_all
    self.commands['reload'] = self.reload

  def reload(self, cid, args):
    os.system('sudo service transmission-daemon reload')

  def connect(self):
    self.tc = transmissionrpc.Client('localhost', port=9091)

  def handle_message(self,cid, command, args):
    try:
      self.commands[command](cid,args)
    except Exception as e:
      self.send_formatted_message(cid,self.get_sorry_message())
      self.log.error(e)

  def get_torrent_list(self, cid, args):
    if not self.tc:
      self.connect()
    message = 'Lista torrent:'
    tlist = self.tc.get_torrents()
    for torrent in tlist:
      message = '%s\nid:*%s) %s %s*' % (message, torrent.id, torrent.name, torrent.status)
    message = '%s\n' % message
    self.send_formatted_message(cid, message)

  def get_torrent_info(self, cid, args): 
    if not self.tc:
      self.connect()
    if len(args) >= 1:
      for torrent in args:
        data = self.get_formatted_torrent_data(torrent)
        self.send_formatted_message(cid, data)
    else:
      self.send_formatted_message(cid,
                                  '*torrent list* usage: torrent list _[TORRENT NUMBER]_...')
 
  def remove_torrent(self, cid, args): 
    if not self.tc:
      self.connect()

    if len(args) >= 1:
      for torrent in args:
        data = self.remove_single_torrent(torrent)
        self.send_formatted_message(cid, data)
    else:
      self.send_formatted_message(cid,
                                  '*torrent remove* usage: torrent remove _[TORRENT NUMBER]_...')

  def remove_single_torrent(self, torrent):
    result = 'Removed torrent with id=*%s*'
    result = result % torrent
    return result

  def start_torrent(self, cid, args): 
    if not self.tc:
      self.connect()

    if len(args) >= 1:
      for torrent in args:
        data = self.start_single_torrent(torrent)
        self.send_formatted_message(cid, data)
    else:
      self.send_formatted_message(cid,
                                  '*torrent start* usage: torrent start _[TORRENT NUMBER]_...')

  def start_single_torrent(self, torrent):
    result = 'Started torrent with id=*%s*'
    self.tc.start_torrent(torrent)
    result = result % torrent
    return result

  def stop_torrent(self, cid, args): 
    if not self.tc:
      self.connect()

    if len(args) >= 1:
      for torrent in args:
        data = self.stop_single_torrent(torrent)
        self.send_formatted_message(cid, data)
    else:
      self.send_formatted_message(cid,
                                  '*torrent stop* usage: torrent stop _[TORRENT NUMBER]_...')

  def stop_single_torrent(self, torrent):
    result = 'Stopped torrent with id=*%s*'
    self.tc.stop_torrent(torrent)
    result = result % torrent
    return result

  def add_torrent(self, cid, args): 
    if not self.tc:
      self.connect()

    if len(args) >= 1:
      for torrent in args:
        data = self.add_single_torrent(torrent)
        self.send_formatted_message(cid, data)
    else:
      self.send_formatted_message(cid,
                                  '*torrent add* usage: torrent list _[TORRENT FILE URI]_...')

  def add_single_torrent(self, torrent):
    result = 'Added *%s* with id=*%s*'
    t = self.tc.add_torrent(torrent);
    result = result % (t.name,t.id)
    return result

  def get_formatted_torrent_data(self, torrent):
    result = 'id:*%s* name:*%s* status:*%s *progress:*%d%%*'
    t = self.tc.get_torrent(int(torrent))
    result = result % (t.id,t.name,t.status,int(t.progress))
    return result

  def start_all(self,cid,args): 
    if not self.tc:
      self.connect()

    self.tc.start_all();
    self.send_formatted_message(cid,'Started *all* torrents')

  def stop_all(self,cid,args): 
    if not self.tc:
      self.connect()

    self.tc.stop_all();
    self.send_formatted_message(cid,'Stopped *all* torrents')

