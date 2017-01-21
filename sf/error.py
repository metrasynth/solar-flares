class SFError(Exception):
    pass


class SFValueError(ValueError, SFError):
    pass
