import sys


def draw(content: list[str]) -> None:
    sys.stdout.write("\033[H\033[J")  # home + clear screen

    for line in content:
        sys.stdout.write(line + "\n")

    sys.stdout.flush()
