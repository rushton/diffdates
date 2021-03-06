from argparse import ArgumentParser
import re
import sys

import ciso8601

ISO_MATCHER = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:Z|[+\-][0-9]{2}:?[0-9]{2})"
)


def diff_dates(line):
    """
    Args:
        line - string line of input to parse dates out of
        unit - unit to return
    Return:
        seconds between dates in a line or None if no dates found
    """

    matches = ISO_MATCHER.findall(line)
    if len(matches) > 1:
        first_date, last_date = [ciso8601.parse_datetime(m) for m in matches[:2]]
        diff = abs(int((first_date - last_date).total_seconds()))
        return diff

    return None


def main():
    """
    entry-point for the program
    """
    parser = ArgumentParser(
        description="finds the difference between two dates in a line of input"
    )
    parser.add_argument(
        "unit",
        nargs="?",
        choices=["seconds", "s", "minutes", "m", "hours", "h", "days", "d"],
        default="s",
        help="defines the unit to format the value of the difference.",
    )
    parser.add_argument(
        "-u",
        "--unbuffered",
        action="store_true",
        help="flush the output after each line is printed.",
    )

    args = parser.parse_args()
    unit = args.unit
    if unit.lower() == "seconds" or unit.lower() == "s":
        unit_divisor = 1
    elif unit.lower() == "minutes" or unit.lower() == "m":
        unit_divisor = 60
    elif unit.lower() == "hours" or unit.lower() == "h":
        unit_divisor = 60 * 60
    elif unit.lower() == "days" or unit.lower() == "d":
        unit_divisor = 60 * 60 * 24
    else:
        raise Exception("invalid unit choice")

    for line in sys.stdin:
        diff_seconds = diff_dates(line)
        if diff_seconds:
            print("%s %.3f" % (line.rstrip(), diff_seconds / unit_divisor))
        else:
            print(line.rstrip())

        if args.unbuffered:
            sys.stdout.flush()


if __name__ == "__main__":
    main()
