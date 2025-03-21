dict_list = {
    'RED': '\x1b[31m',
    'GREEN': '\x1b[32m',
    'YELLOW': '\x1b[33m',
    'BLUE': '\x1b[34m',
}
BOLD = '\x1b[1m'
RESET = '\x1b[0m'
UNDERLINE = '\x1b[4m'
CLEAR_SCREEN = '\x1b[2J'


def underline(color: str):
    return UNDERLINE if color.upper() != 'BLUE' else ''


def colorize(text: str, color: str):
    return_c = dict_list[color.upper()]
    return str(return_c + underline(color) + BOLD + str(text) + RESET)
