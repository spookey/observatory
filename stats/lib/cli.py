import click
from flask import Blueprint

from stats.lib.text import is_slugable
from stats.models.user import User

BP_CLI = Blueprint('cli', __name__)


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
