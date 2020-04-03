from flask.helpers import get_debug_flag

from observatory.app import create_app
from observatory.start.config import DevelopmentConfig, ProductionConfig

APP = create_app(
    DevelopmentConfig if get_debug_flag() else ProductionConfig
)
