import sys

from .token import validate

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Example: python -m sympla_tools.tickets.signature.token.validate <signature>"
        )
        sys.exit(1)

    signature = sys.argv[1]
    validate(signature)
