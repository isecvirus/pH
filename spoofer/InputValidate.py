import re


def IP_VALIDATOR(event):
    # IR = IP REGEX
    IR = re.compile('('
                    '^\d{0,3}$|'
                    '^\d{0,3}\.\d{0,3}$|'
                    '^\d{0,3}\.\d{0,3}\.\d{0,3}$|'
                    '^\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}$'
                    ')')
    if IR.match(event):
        return True
    return False