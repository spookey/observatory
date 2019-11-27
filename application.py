from flask.helpers import get_debug_flag

from stats.app import create_app
from stats.start.config import DevelopmentConfig, ProductionConfig

APP = create_app(
    DevelopmentConfig if get_debug_flag() else ProductionConfig
)
