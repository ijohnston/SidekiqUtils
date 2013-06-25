"""

author:  Isaac Johnston
date  :  June 19, 2013

"""
import urllib2
import urlparse
from datetime import datetime
from shelve import DbfilenameShelf
from xml.dom.minidom import parseString

from mydatetime import utc_to_local
from myminidom import get_node_text


class SidekiqPoller(object):
    """
    Use the class SidekiqPoller to poll sidekiq for status of workers, etc.
    using the web API.

    Usage:
    from sidekiqutils import SidekiqPoller

    poller = SidekiqPoller('myname', 'mypass', 'myserverurl')
    workers = poller.get_workers()
    w = workers[0]
    worker, worker_id, started = w['worker'], w['id'], w['started']
    dumped = poller.dump_workers('/path/to/file.dbm', workers)
    worker, started, asset_id = dumped[0]
    loaded = poller.load_workers('/path/to/file.dbm')
    worker, started, asset_id = loaded[0]

    """
    def __init__(self,
                 username,
                 password,
                 base_url='http://doc-1.caplinked.com/sidekiq/'):
        """
        Constructor.

        Args:
        username -- the user name.
        password -- the password.
        base_url -- the URL of the doc server.  Defaults to prod.

        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.workers_url = urlparse.urljoin(base_url, 'workers')
        self._opener = None

    @property
    def opener(self):
        """
        Return a urllib2.OpenerDirector instance configured for self.base_url.
    
        """
        if not self._opener:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                None, self.base_url, self.username, self.password
            )
            auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            self._opener = urllib2.build_opener(auth_handler)
        return self._opener

    def dump_workers(self, filename, workers):
        """
        Write a sequence of workers written to disk, e.g.
        [(id, started, assetid),...], and then return the sequence.

        """
        seq = []
        for w in workers:
            seq.append((w['worker'], w['started'], w['args'][1]))
        shelf = DbfilenameShelf(filename)
        shelf['workers'] = seq 
        shelf.close()
        return seq
    
    def get_workers(self):
        """
        Return a list of dicts for each active worker or an empty list if none.

        """
        resp = self.opener.open(self.workers_url)
        document = parseString(resp.read())
        time_fmt = '%Y-%m-%dT%H:%M:%SZ'
        workers = []
        for row in document.getElementsByTagName('tr'):
            cells = row.getElementsByTagName('td')
            worker = {}
            worker['worker'] = get_node_text(row, 'td', 0).strip()
            worker['queue'] = get_node_text(row, 'a', 0).strip()
            worker['class'] = get_node_text(row, 'td', 2).strip()
            worker['id'] = row.getElementsByTagName('div')[0].getAttribute('id')
            worker['args'] = eval(get_node_text(row, 'div').strip())
            # Convert started time from utc to local.
            utc_str = row.getElementsByTagName('time')[0] \
                    .getAttribute('datetime')
            utc_dt = datetime.strptime(utc_str, time_fmt)
            local_dt = utc_to_local(utc_dt)
            worker['started'] = local_dt.strftime(time_fmt)[:-1]
            workers.append(worker)
        return workers

    def load_workers(self, filename):
        """
        Return a list of workers read from disk as [(id, started, assetid),...].

        """
        shelf = DbfilenameShelf(filename)
        try:
            workers = shelf['workers']
        except:
            workers = []
        shelf.close()
        return workers
