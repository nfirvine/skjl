import argparse
import sys
import logging
_log = logging.getLogger('skjlcli' if __name__ == '__main__' else __name__)

import skjl.importer
import skjl.db
import skjl.cfg

CFG_PREFIX = 'cfg:'


def do_init(args, cfg):
    _log.info('Creating db')
    db = skjl.db.Connection(cfg['db']).create(force=args.force)
    _log.info('Created db')


def do_imp(args, cfg):
    _log.info('Importing from "%s"', args.input)
    db = skjl.db.Connection(cfg['db'])
    for inp in args.input:
        if inp == '-':
            inp = [sys.stdin]
        elif inp.startswith(CFG_PREFIX):
            inp = cfg[inp.split(CFG_PREFIX)[1]]
        skjl.importer.imp(db, args.type, inp)
    db.flush()


def cli(argv=sys.argv):
    ap = argparse.ArgumentParser(prog='skjlcli')
    ap.add_argument('--config', '-c', default=skjl.cfg.DEFAULT_PATH)
    ap.add_argument('--verbose', '-v', action='store_true')
    sp = ap.add_subparsers()

    init = sp.add_parser('init')
    init.add_argument('--force', '-f', action='store_true')
    init.set_defaults(func=do_init)

    imp = sp.add_parser('import')
    imp.add_argument('--type', '-t', choices=skjl.importer.importers.keys(), default='skjlhuman')
    input_default = CFG_PREFIX+'input'
    imp.add_argument('input', default=[input_default], nargs='*')
    imp.set_defaults(func=do_imp)

    args = ap.parse_args(argv[1:])
    logging.basicConfig()
    if args.verbose:
        _log.setLevel(logging.DEBUG)
    cfg = skjl.cfg.load(args.config)
    args.func(args, cfg)


if __name__ == '__main__':
    cli()
