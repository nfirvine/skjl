import yaml

import skjl.core

importers = {}

class SkjlHuman(object):
    DB_VERSION = '0'
    def __init__(self, db):
        assert db['_version'] == self.DB_VERSION
        self.db = db

    def imp(self, infile):
        docs = yaml.load_all(infile)
        for doc in docs:
            typ, body = doc.items()[0]
            getattr(self, '_imp_%s' % typ)(body)

    def _imp_tasks(self, tasks):
        #TODO: create subtasks, etc.
        for task in tasks:
            return skjl.core.Task.create(self.db, task)
importers['skjlhuman'] = SkjlHuman

def imp(db, typ, infile):
    imper = importers[typ](db)
    imper.imp(infile)
