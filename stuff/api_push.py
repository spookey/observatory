#!/usr/bin/env python3

from argparse import ArgumentParser
from json import dumps, loads
from sys import exit as _exit
from urllib.request import (
    HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm, Request,
    build_opener, install_opener, urlopen
)


def arguments():
    parser = ArgumentParser(__file__, add_help=True, epilog='🦆 🦆 🦆')
    parser.add_argument(
        '-b', '--base', type=str,
        default='http://localhost:5000', help='base url (%(default)s)',
    )
    parser.add_argument(
        '-s', '--slug', type=str,
        required=True, help='sensor slug',
    )
    parser.add_argument(
        '-v', '--value', type=float,
        required=True, help='point value',
    )
    parser.add_argument(
        '-u', '--user', type=str, dest='username',
        required=True, help='api username',
    )
    parser.add_argument(
        '-p', '--pass', type=str, dest='password',
        required=True, help='api password',
    )
    return parser.parse_args()


def main():
    args = arguments()
    args.base = args.base.rstrip('/')

    manager = HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, args.base, args.username, args.password)
    install_opener(build_opener(HTTPBasicAuthHandler(manager)))

    url = f'{args.base}/api/sensor/{args.slug}'
    data = dumps({'value': args.value}, allow_nan=True).encode()
    headers = {'Content-Type': 'application/json'}

    req = Request(url=url, data=data, headers=headers, method='POST')
    with urlopen(req, timeout=5) as res:
        print(f'{res.status} {res.reason}')
        print(loads(res.read().decode()))

    return 0


if __name__ == '__main__':
    _exit(main())
