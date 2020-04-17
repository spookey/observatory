from os import getenv, path

from observatory.lib.parse import parse_int, parse_str_bool

APP_NAME = 'observatory'
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

BCRYPT_LOG_ROUNDS = parse_int(getenv('BCRYPT_LOG_ROUNDS', '13'), fallback=13)

CSRF_STRICT = parse_str_bool(getenv('CSRF_STRICT', 'true'), fallback=True)

BACKLOG_DAYS = parse_int(getenv('BACKLOG_DAYS', '14'), fallback=True)

TITLE = getenv('TITLE', 'Observatory')
HTML_LANG = getenv('HTML_LANG', 'en')
FAVICON = getenv('FAVICON', 'logo.png')

FMT_STRFTIME = getenv('FMT_STRFTIME', '%d.%m.%Y %H:%M:%S UTC')
FMT_MOMENT = getenv('FMT_MOMENT', 'DD. MMM YYYY HH:mm:ss')

TAGLINES = [
    getenv('TAGLINE_01', 'Hey Peter, what\'s happening?'),
    getenv('TAGLINE_02', 'Someone set us up the bomb!'),
    getenv('TAGLINE_03', 'We get signal!'),
    getenv('TAGLINE_04', 'Terror as a business!'),
    getenv('TAGLINE_05', 'Looking at numbers!'),
    getenv('TAGLINE_06', 'Rage against the virtual machine.'),
]

ICON = {
    '__fallback': getenv('ICON___FALLBACK', 'fire'),
    'bool_right': getenv('ICON_BOOL_RIGHT', 'check'),
    'bool_wrong': getenv('ICON_BOOL_WRONG', 'close'),
    'glob_descr': getenv('ICON_GLOB_DESCR', 'more'),
    'glob_empty': getenv('ICON_GLOB_EMPTY', 'emotion-sad'),
    'glob_error': getenv('ICON_GLOB_ERROR', 'flashlight'),
    'obj_mapper': getenv('ICON_OBJ_MAPPER', 'guide'),
    'obj_prompt': getenv('ICON_OBJ_PROMPT', 'newspaper'),
    'obj_sensor': getenv('ICON_OBJ_SENSOR', 'radar'),
    'ops_arr_dn': getenv('ICON_OPS_ARR_DN', 'arrow-down-s'),
    'ops_arr_up': getenv('ICON_OPS_ARR_UP', 'arrow-up-s'),
    'ops_create': getenv('ICON_OPS_CREATE', 'add'),
    'ops_delete': getenv('ICON_OPS_DELETE', 'delete-bin'),
    'ops_submit': getenv('ICON_OPS_SUBMIT', 'check-double'),
    'user_basic': getenv('ICON_USER_BASIC', 'user'),
    'user_enter': getenv('ICON_USER_ENTER', 'login-box'),
    'user_leave': getenv('ICON_USER_LEAVE', 'logout-box-r'),
}

ERROR_CODES = (
    400, 401, 403, 404, 418,
    500, 501, 502, 503, 504,
)
