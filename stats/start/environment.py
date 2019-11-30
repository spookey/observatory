from os import getenv, path

from stats.start.helper import parse_bool, parse_int

APP_NAME = 'stats'
MDL_NAME = __name__.split('.')[0]

THIS_DIR = path.abspath(path.dirname(__file__))
BASE_DIR = path.abspath(path.dirname(THIS_DIR))
ROOT_DIR = path.abspath(path.dirname(BASE_DIR))

LOG_LVL = getenv('LOG_LVL', 'info')

MIGR_DIR = path.abspath(path.join(ROOT_DIR, 'migrate'))

DATABASE = getenv('DATABASE', 'sqlite://')
DATABASE_DEV = getenv('DATABASE_DEV', 'sqlite:///{}'.format(
    path.abspath(path.join(ROOT_DIR, 'database_dev.sqlite'))
))

SECRET_FILE = getenv('SECRET_FILE', 'secret.key')
SECRET_BASE = getenv('SECRET_BASE', ROOT_DIR)

CSRF_STRICT = parse_bool(getenv('CSRF_STRICT', 'true'), fallback=True)

BACKLOG_DAYS = parse_int(getenv('BACKLOG_DAYS', '14'), fallback=True)

TITLE = getenv('TITLE', APP_NAME)
HTML_LANG = getenv('HTML_LANG', 'en')

ERROR_CODES = (
    400, 401, 403, 404, 418,
    500, 501, 502, 503, 504,
)
