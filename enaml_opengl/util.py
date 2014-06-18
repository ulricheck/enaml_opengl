__author__ = 'jack'
import traceback
import time

def get_exception(indent=4, prefix='|  '):
    tb = traceback.format_exc()
    lines = []
    for l in tb.split('\n'):
        lines.append(" "*indent + prefix + l)
    return '\n'.join(lines)

def print_exception(msg='', indent=4, prefix='|'):
    """Print an error message followed by an indented exception backtrace
    (This function is intended to be called within except: blocks)"""
    exc = get_exception(indent, prefix + '  ')
    print("[%s]  %s\n" % (time.strftime("%H:%M:%S"), msg))
    print(" "*indent + prefix + '='*30 + '>>')
    print(exc)
    print(" "*indent + prefix + '='*30 + '<<')
