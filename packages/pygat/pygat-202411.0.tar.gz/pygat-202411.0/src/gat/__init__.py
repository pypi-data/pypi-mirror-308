from datetime import datetime

__VERSION_SUFFIX = '.0'


def version():
    return datetime.now().strftime('%Y%m') + __VERSION_SUFFIX
