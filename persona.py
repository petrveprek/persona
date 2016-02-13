#!python3
"""persona"""

import sys
import time


def main():
    print("*** persona ***")
    print("Python {}".format(sys.version))
    print("Started at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    started_at = time.time()

    print("Completed at {}".format(time.strftime("%Y-%m-%d %H:%M:%S")))
    elapsed = time.time() - started_at
    seconds = round(elapsed)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    print("Elapsed {:d}w {:d}d {:d}h {:d}m {:d}s ({:,.3f}s)".format(weeks, days, hours, minutes, seconds, elapsed))

if __name__ == '__main__':
    main()
