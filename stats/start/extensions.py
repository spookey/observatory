from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from stats.start.environment import MIGR_DIR

BCRYPT = Bcrypt()
CSRF_PROTECT = CSRFProtect()
DB = SQLAlchemy()
LOGIN_MANAGER = LoginManager()
MIGRATE = Migrate(directory=MIGR_DIR)
