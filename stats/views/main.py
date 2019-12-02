from flask import Blueprint, current_app, render_template

from stats.models.user import User
from stats.start.extensions import LOGIN_MANAGER

BLUEPRINT_MAIN = Blueprint('main', __name__)


@LOGIN_MANAGER.user_loader
def user_loader(prime):
    return User.by_prime(prime)
