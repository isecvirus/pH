import datetime

DEFAULT = 0
IMPORTANT = 1
SUCCESS = 2
INFO = 3
ERROR = 4
WARNING = 5
IGNORE = 6


def dbg(msg, type: int = 0):
    types = [
        "\033[97m",  # DEFAULT -> white
        "\033[5m",  # IMPORTANT -> blink
        "\033[92m",  # SUCCESS -> green
        "\033[96m",  # INFO -> cyan
        "\033[91m",  # ERROR -> red
        "\033[93m",  # WARNING -> yellow
        "\033[90m"  # IGNORE -> gray
    ]
    color = types[type]
    print(f"\033[1m»\033[0m \033[1m[\033[0m{color}\033[1m%s\033[0m\033[1m]\033[0m %s" % (
        datetime.datetime.now().strftime("%I:%M:%S"), msg))
