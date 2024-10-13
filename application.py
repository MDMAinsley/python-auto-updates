import sys

__version__ = "2.0.0"


# Main Function
def main():
    if "--version" in sys.argv:
        print(f"v{__version__}")
        return
    print(f"Running application version v{__version__}")


if __name__ == "__main__":
    main()
