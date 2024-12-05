import json
import logging
import os
import sys

import sha3
from eth_account import Account
from web3 import Web3


logging.basicConfig(
    level=logging.DEBUG,  # Define o nível de log para DEBUG ou outro nível desejado
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]  # Redireciona os logs para a saída padrão
)

KNOWN_ETHEREUM_ADDRESS = os.getenv(
    "KNOWN_ETHEREUM_ADDRESS", "0x0ff5a47F678e1E490b9c467631Ab84Dc1665a7eA"
)

if not KNOWN_ETHEREUM_ADDRESS:
    raise ValueError("KNOWN_ETHEREUM_ADDRESS is not set")


def keccak_256(data):
    keccak = sha3.keccak_256()
    keccak.update(data)
    return keccak.digest()


def add_ethereum_prefix(message):
    serialized_message = json.dumps(
        message, separators=(",", ":"), sort_keys=False
    )
    logging.debug(f"\n[DEBUG] Serialized JSON Message: {serialized_message}")

    prefix = f"\u0019Ethereum Signed Message:\n{len(serialized_message)}"
    prefixed_message = prefix.encode("utf-8") + serialized_message.encode(
        "utf-8"
    )
    logging.debug(f"[DEBUG] Prefixed Message: {prefixed_message}")

    message_hash = keccak_256(prefixed_message)
    logging.debug(f"[DEBUG] Message hash (hex): {message_hash.hex()}")
    return message_hash


def validate(message_json, signature):
    logging.debug(
        f"\n[DEBUG] Original Message JSON: {message_json}"
        f"[DEBUG] Signature: {signature}"
    )

    if isinstance(message_json, str):
        message_json = json.loads(message_json)

    message_hash = add_ethereum_prefix(message_json)

    signature = signature[2:] if signature.startswith("0x") else signature
    r = bytes.fromhex(signature[:64])
    s = bytes.fromhex(signature[64:128])
    v = int(signature[128:130], 16)

    if v < 27:
        v += 27

    logging.debug(
        f"[DEBUG] Message hash (hex): {message_hash.hex()}"
        f"[DEBUG] r (hex): {r.hex()}"
        f"[DEBUG] s (hex): {s.hex()}"
        f"[DEBUG] v: {v}"
    )

    try:
        recovered_address = Account._recover_hash(message_hash, vrs=(v, r, s))

        logging.debug(
            f"[DEBUG] Recovered Address: {recovered_address}"
            f"[DEBUG] Known Ethereum Address: {KNOWN_ETHEREUM_ADDRESS}"
        )

        is_valid = Web3.to_checksum_address(
            recovered_address
        ) == Web3.to_checksum_address(KNOWN_ETHEREUM_ADDRESS)
        logging.debug(f"[DEBUG] Is the signature valid? {is_valid}")

        print("Valid signature.")

        return is_valid
    except Exception as e:
        print("Inavalid signature.")
        logging.debug(f"[ERROR] Error validating signature: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Example: python -m sympla_tools.tickets.signature.token validate <message> <signature>")
        sys.exit(1)

    command = sys.argv[1]
    message_json = sys.argv[2]
    signature = sys.argv[3]

    if command != "validate":
        print("Invalid command.")
        sys.exit(1)

    logging.debug(
        f"Command: {command} "
        f"Signature: {signature} "
        f"message: {message_json}"
    )

    validate(message_json, signature)
