import re
import urlparse
import os
import errno
import yaml
import logging
_log = logging.getLogger(__name__)

class Connection(object):
    handlers = []
    def __init__(self, uri):
        self._db = self.get_handler(uri)(uri)

    @classmethod
    def get_handler(cls, uri):
        for r, h in cls.handlers:
            if r.match(uri):
                return h
        raise ValueError('No handler found for url "%s"' % uri)

    @classmethod
    def add_handler(cls, regex, yourclass):
        cls.handlers.append((re.compile(regex), yourclass))

    def flush(self):
        self._db.flush()

    def create(self, force=False):
        return self._db.create(force)

    def __getitem__(self, k):
        return self._db[k]


class YamlDb(object):
    VERSION = 1
    def __init__(self, uri):
        self._uri = uri
        p = urlparse.urlparse(uri)
        self._backing = p.path
        self._db = {}

    def __getitem__(self, k):
        return self._db[k]

    def flush(self):
        with open(self._backing, 'w') as f:
            yaml.dump(self._db, f)

    def create(self, force=False):
        self._db = {
            '_version': self.VERSION,
            'tasks': {},
            'contexts': {},
        }
        try:
            os.mkdir(os.path.dirname(self._backing))
        except OSError as exc:
            if not exc.errno == errno.EEXIST and not force:
                raise
        exists = os.path.exists(self._backing)
        if exists and not force:
            raise IOError("db already exists: %s" % self._backing)
        else:
            _log.info("Created db at %s" % self._backing)
        self.flush()

    def load(self):
        with open(self._backing, 'r') as f:
            self._db = yaml.load(f)

Connection.add_handler(r'file://.*', YamlDb) 
