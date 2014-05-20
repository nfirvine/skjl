import yaml
import os
import logging
import urlparse

_log = logging.getLogger(__name__)

def mkfn(name, where='data'):
    if where == 'data':
        return os.path.join(
            os.environ.get('XDG_DATA_HOME', '~/.local/share/'),
            'skjl',
            name
        )
    elif where == 'cfg':
        return os.path.join(
            os.environ.get('XDG_CONFIG_HOME', '~/.config/'),
            name
        )
    else:
        raise ValueError('bad resource location "%s"' % where)


DEFAULT_PATH = mkfn('skjl.yaml', 'cfg')
DEFAULTS = {
    'db': mkfn('db.yaml'),
    'input': mkfn('input.yaml'),
}
TYPES = {
    'db': 'uri',
    'input': 'path'
}

def coerce(key, val, type=None):
    def normalize_path(path):
         return os.path.abspath(os.path.expanduser(path))

    if type is None:
        type = TYPES[key]
    if type == 'path':
        return key, normalize_path(val)
    elif type == 'uri':
        parsed = urlparse.urlparse(val)
        scheme = parsed.scheme
        path = parsed.path
        if scheme == '':
            scheme = 'file'
        if scheme == 'file':
            path = normalize_path(path)
        return key, urlparse.urlunparse(urlparse.ParseResult(
            scheme=scheme, 
            netloc=parsed.netloc,
            path=path,
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment,
        ))
    else:
        return key, val

def load(path=DEFAULT_PATH):
    try:
        with open(path, 'r') as f:
            data = yaml.load(f)
    except IOError as exc:
        if path != DEFAULT_PATH:
            raise
        else:
            data = {}
    cfg = {}
    cfg.update(coerce(k, v) for k, v in DEFAULTS.iteritems())
    cfg.update(coerce(k, v) for k, v in data.iteritems())
    return cfg
