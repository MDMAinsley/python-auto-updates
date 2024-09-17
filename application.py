import sys

__version__ = "1.0.2"


def main():
    if "--version" in sys.argv:
        print(f"v{__version__}")
        return
    print(f"Running application version v{__version__}")


if __name__ == "__main__":
    main()
