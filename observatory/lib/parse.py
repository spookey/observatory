from logging import getLogger

STR_TRUTHY = ('true', '1', 'on', 'banana')
STR_FALSY = ('false', '0', 'off')
LOG = getLogger(__name__)


def parse_int(value, fallback=0, warn=True):
    try:
        value = int(value)
    except (ValueError, TypeError) as ex:
        if warn:
            LOG.exception(ex)
            LOG.warning(
                'cannot parse "%s" - using fallback "%s"',
                value, fallback
            )
        return fallback
    return value


def parse_bool(value, fallback=False, warn=True):
    try:
        value = value.lower()
    except AttributeError as ex:
        if warn:
            LOG.exception(ex)
            LOG.warning(
                'cannot parse "%s" - using fallback "%s"',
                value, fallback
            )
        return fallback
    if value in STR_TRUTHY:
        return True
    if value in STR_FALSY:
        return False
    if warn:
        LOG.warning(
            'unknown value "%s" - using fallback "%s"',
            value, fallback
        )
    return fallback


def parse_num_bool(value, fallback=False, warn=True):
    value = parse_int(value, fallback=fallback, warn=warn)
    if value == fallback:
        return fallback
    return bool(value)
