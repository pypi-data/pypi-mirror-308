from datetime import datetime

__VERSION_SUFFIX = '.1'


def version():
    return datetime.now().strftime('%Y%m') + __VERSION_SUFFIX
