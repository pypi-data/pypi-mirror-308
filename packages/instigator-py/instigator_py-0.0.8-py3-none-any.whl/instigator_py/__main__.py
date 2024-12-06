"""Allow instigator_py to be executable through `python -m instigator_py`."""

from instigator_py.cli import main

if __name__ == "__main__":
    main(prog_name="instigator_py")
