import skjl.db
import collections

class DbObject(collections.Mapping):
    def __init__(self, _id, **kwargs):
        self._data = {
            '_id': _id
        }
        self._data.update(kwargs)

    def __getitem__(self, k):
        return self._data[k]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def replace(self, db):
        db[self._id] = dict(self)

    @classmethod
    def create(cls, dbcon, name, id_hint='', **kwargs):
        """Creates a task in the database"""
        _id = dbcon.allocate_id(id_hint)
        o = cls(_id, name, **kawargs) 
        return o

    @classmethod
    def yaml_construct(cls, loader, node):
        mapping = loader.construct_mapping(node)
        _id = mapping.pop('_id')
        return cls(_id, **mapping)

    @staticmethod
    def yaml_represent(dumper, inst):
        data = dict(inst)
        return dumper.represent_mapping(data)

def Task(DbObject):
    def __init__(self, _id, name, desc='', resources=[], 
            after=None, before=None, done=False, butfirst=[], andthen=[]):
        super(Task, self).__init__(
            _id,
            name=name,
            desc=desc,
            resources=resources,
            after=after,
            before=before,
            done=done,
            butfirst=butfirst,
            andthen=andthen,
        )
