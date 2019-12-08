from logging import getLogger

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from stats.forms.user import LoginForm
from stats.models.user import User
from stats.start.extensions import LOGIN_MANAGER

BLUEPRINT_USER = Blueprint('user', __name__)
LOG = getLogger(__name__)


@LOGIN_MANAGER.user_loader
def user_loader(prime):
    return User.by_prime(prime)


@BLUEPRINT_USER.route('/logout')
@login_required
def logout():
    LOG.info('logout for user "%s"', current_user.username)
    logout_user()
    flash('See you soon!', 'dark')
    return redirect(url_for('main.index'))


@BLUEPRINT_USER.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.action():
            flash('Welcome back!', 'dark')
            return redirect(
                request.args.get('next') or url_for('main.index')
            )

    return render_template(
        'user/login.html',
        title='Tickets, please!',
        form=form
    )
