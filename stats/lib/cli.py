import click
from flask import Blueprint

from stats.models.user import User

BP_CLI = Blueprint('cli', __name__)


@BP_CLI.cli.command('adduser', help='Add new user')
@click.option('--username', prompt=True)
@click.password_option('--password')
def adduser(username, password):
    if User.by_username(username) is not None:
        click.secho(f'{username} already present!', fg='red')
        return

    user = User.create(username=username, password=password)
    user.save()
    click.echo(f'{username} created!')


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
    click.echo(f'password changed for {username}!')


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

    st_txt = 'active' if state else 'blocked'
    click.echo(f'state changed to {st_txt} for {username}!')
