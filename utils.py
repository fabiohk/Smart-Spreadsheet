import sys


def suppress_stderr():
    def nothing(*args):
        pass

    sys.stderr.write = nothing
