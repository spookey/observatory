from datetime import datetime
from math import pi, sin

import click
from flask import Blueprint

from observatory.lib.clock import epoch_seconds
from observatory.lib.text import is_slugable
from observatory.models.point import Point
from observatory.models.sensor import Sensor
from observatory.models.user import User
from observatory.start.extensions import DB

BP_CLI = Blueprint('cli', __name__)

# pylint: disable=no-member


@BP_CLI.cli.command('adduser', help='Add new user')
@click.option('--username', prompt=True)
@click.password_option('--password')
def adduser(username, password):
    if User.by_username(username) is not None:
        click.secho(f'{username} already present!', fg='red')
        return

    if not is_slugable(username):
        click.secho(f'{username} is an invalid name!', fg='red')
        return

    user = User.create(username=username, password=password)
    user.save()
    click.secho(f'{username} created!', fg='green')


@BP_CLI.cli.command('setpass', help='Set password of user')
@click.option('--username', prompt=True)
@click.password_option('--password')
def setpass(username, password):
    user = User.by_username(username)
    if user is None:
        click.secho(f'{username} not found!', fg='red')
        return

    user.set_password(password)
    user.save()
    click.secho(f'password changed for {username}!', fg='green')


@BP_CLI.cli.command('setstate', help='Toggle active state of user')
@click.option('--username', prompt=True)
@click.option('--active/--blocked', 'state', default=True)
def setstate(username, state):
    user = User.by_username(username)
    if user is None:
        click.secho(f'{username} not found!', fg='red')
        return

    user.active = state
    user.save()
    state = 'active' if state else 'blocked'
    click.secho(f'state changed to {state} for {username}!', fg='green')


@BP_CLI.cli.command('sensorclear', help='Remove all points from sensor')
@click.option('--slug', prompt=True)
def sensorclear(slug):
    sensor = Sensor.by_slug(slug)
    if not sensor:
        click.secho(f'{slug} not present!', fg='red')
        return

    number = Point.query.with_parent(sensor).delete()
    DB.session.commit()
    click.echo(f'deleted {number} points from {slug}')


@BP_CLI.cli.command('sensorcurve', help='Draw a curve of points on sensor')
@click.option('--slug', prompt=True)
@click.option('--axc', type=int, default=15)
@click.option('--keep-old', is_flag=True, default=False)
def sensorcurve(slug, axc, keep_old):
    sensor = Sensor.by_slug(slug)
    if not sensor:
        click.secho(f'{slug} not present!', fg='red')
        return

    if not keep_old:
        sensor.cleanup(_commit=False)

    num = 1 + 2 * axc
    sec = epoch_seconds(datetime.utcnow())
    for pos in range(0, -num, -1):
        value = round(sin((1 / axc) * pos * pi), 8)
        stamp = datetime.utcfromtimestamp(sec + pos)

        Point.create(
            sensor=sensor,
            created=stamp,
            value=value,
            _commit=False,
        )

    DB.session.commit()
    click.echo(f'created {num} points for {slug}')
