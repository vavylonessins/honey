import sys
from const import *
import traceback as tb


class params:
    ignored_warnings: list[str] = []
    debug_mode: bool = False
    exit_status: int = SUCCESS_CODE
    args: list = []
    code: str = ""
    main_file: str = ""


def handle_args():
    global args
    args = []

    for a in sys.argv:
        if not a.startswith("py") and not a.startswith("hny") and not a.startswith("main"):
            args.append(a)
    
    if "--help" in args:
        print_help()
    
    if not args:
        print_help()
    
    if "--debug" in args:
        params.debug_mode = True


def print_help():
    print(HELP)
    sys.exit(SUCCESS_CODE)


def error(errtype, token, comment=""):
    print(errtype + " in file \"%s\", line %d:" % (params.main_file, token.line(params.code)))
    print("│   " + params.code.splitlines()[token.line(params.code) - 1])
    print("│   " + " " * (token.column(params.code)) + "^")
    print("╰───" + "-" * (token.column(params.code)) + "╯")
    print(comment, sep=("","\n")[1 if comment else 0])
    sys.exit(ERRORS_CODE)


def warning(warntype, token, comment=""):
    print(warntype + " in file \"%s\", line %d:" % (params.main_file, token.line(params.code)))
    print("│   " + params.code.splitlines()[token.line(params.code)])
    print("│   " + " " * (token.column(params.code)) + "^")
    print("╰───" + "-" * (token.column(params.code)) + "╯")
    print(comment, sep=("","\n")[1 if comment else 0])
    global exit_status
    exit_status = WARNINGS_CODE


def panic(exc):
    stack = tb.extract_stack()
    stack.pop()
    print("Traceback (most recent call last):")
    print('\n'.join(tuple(tb.format_stack())[:-2])[:-1])
    print('\n'.join(tuple(tb.format_exception_only(exc))))
    sys.exit(CRUSH_CODE)


def log(*a):
    if params.debug_mode:
        print("[*]", *a, "\n")
