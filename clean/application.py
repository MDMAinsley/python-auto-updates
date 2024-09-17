import sys

__version__ = "1.0.0"


def main():
    if "--version" in sys.argv:
        print(__version__)
        return
    print("Running application version", __version__)
    input("Main Launched.")


if __name__ == "__main__":
    main()
