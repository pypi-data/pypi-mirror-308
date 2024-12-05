import sys

from sympla_tools.tickets.qrcode_signature import validate


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m sympla_tools.tickets <signature>")
        sys.exit(1)

    signature = sys.argv[1]
    message_json = '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"37884525610813"}'

    # Chamando a função de validação
    is_valid = validate(message_json, signature)
    if is_valid:
        print("Signature is valid.")
    else:
        print("Signature is invalid.")


if __name__ == "__main__":
    main()
