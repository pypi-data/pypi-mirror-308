import json
import logging
import os
import sys

from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils.curried import keccak
from web3 import Web3

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "ERROR"),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

KNOWN_ETHEREUM_ADDRESS = Web3.to_checksum_address(
    os.getenv(
        "KNOWN_ETHEREUM_ADDRESS", "0xdB074b3c323A7Ad418EBBe66baD231f43f680563"
    )
)

if not KNOWN_ETHEREUM_ADDRESS:
    raise ValueError("KNOWN_ETHEREUM_ADDRESS is not set")


def validate(original_message_json, signature_hex):
    logging.debug("\n\n\nValidating signature...")

    signature_hex = (
        signature_hex[2:] if signature_hex.startswith("0x") else signature_hex
    )

    try:
        message_dict = json.loads(original_message_json)

        if not message_dict.get("address") or not message_dict.get(
            "ItemTypeId"
        ):
            print("Invalid message.")
            return False

        dict_message_json_ordered = {
            "address": message_dict.get("address"),
            "ItemTypeId": message_dict.get("ItemTypeId"),
        }
        message_json = json.dumps(
            dict_message_json_ordered, separators=(",", ":")
        )

        logging.debug(
            f"Original Message JSON: {original_message_json} \n"
            f"Dict Message: {message_dict} \n"
            f"Ordered Message: {dict_message_json_ordered} \n"
            f"Final Message JSON for Signing: {message_json} \n"
            f"Signature: {signature_hex} \n"
        )

        if len(signature_hex) != 130:
            logging.debug("Signature must have 130 characters. \n")
            print("Invalid signature.")
            return False

        message_hash = keccak(text=message_json)

        encoded_message = encode_defunct(hexstr=message_hash.hex())

        r = int(signature_hex[0:64], 16)
        s = int(signature_hex[64:128], 16)
        v = int(signature_hex[128:130], 16)

        logging.debug(
            f"Signature components \n"
            f"r: {hex(r)} \n"
            f"s: {hex(s)} \n"
            f"v: {v} \n"
        )

        recovered_address = Account.recover_message(
            encoded_message, vrs=(v, r, s)
        )
        checksum_recovered_address = Web3.to_checksum_address(
            recovered_address
        )

        logging.debug(
            f"Recovered address: {recovered_address} \n"
            f"checksum_recovered_address: {checksum_recovered_address} \n"
            f"checksum_known_address: {KNOWN_ETHEREUM_ADDRESS} \n"
        )

        if checksum_recovered_address != KNOWN_ETHEREUM_ADDRESS:
            print("Invalid signature.")
            return False

        print("Valid signature.")
        return True

    except Exception as e:
        logging.error("Invalid signature", exc_info=True)
        print("Invalid signature.")
        return False


if __name__ == "__main__":

    command = sys.argv[1]
    message_json = sys.argv[2]
    signature_hex = sys.argv[3]

    if command != "validate":
        print("Invalid command.")
        sys.exit(1)

    logging.debug(
        f"Command: {command} "
        f"Signature: {signature_hex} "
        f"message: {message_json}"
    )

    ethereum_address = validate(message_json, signature_hex)

    print(ethereum_address)
