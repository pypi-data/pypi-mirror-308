import json
import logging
import os
import sys

from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "ERROR"),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

KNOWN_ETHEREUM_ADDRESS = os.getenv(
    "KNOWN_ETHEREUM_ADDRESS", "0xce965894a2376735df159c8a162624791987f759"
)

if not KNOWN_ETHEREUM_ADDRESS:
    raise ValueError("KNOWN_ETHEREUM_ADDRESS is not set")


def validate(original_message_json, signature_hex):
    try:
        message_dict = json.loads(original_message_json)

        if not message_dict.get("address") or not message_dict.get(
            "ItemTypeId"
        ):
            logging.debug("Invalid message.")
            print("Invalid message.")
            return False

        dict_message_json_ordered = {
            "address": message_dict.get("address"),
            "ItemTypeId": message_dict.get("ItemTypeId"),
        }
        message_json = json.dumps(dict_message_json_ordered).replace(" ", "")

        logging.debug(
            f"\nOriginal Message JSON: {original_message_json} "
            f"\nDict Message: {message_dict} "
            f"\nOrdered Message: {dict_message_json_ordered} "
            f"\nLast Message: {message_json} "
            f"\nSignature: {signature_hex}"
        )

        if len(signature_hex) < 132:
            logging.debug("Signature must have 132 characters.")
            print("Inavalid signature.")
            return False

        encoded_message = encode_defunct(text=message_json)

        signature_hex = (
            signature_hex[2:]
            if signature_hex.startswith("0x")
            else signature_hex
        )

        recovered_address = Account.recover_message(
            encoded_message, signature=signature_hex
        )

        print("Recovered ethereum address:", recovered_address)

        if Web3.to_checksum_address(
            recovered_address
        ) != Web3.to_checksum_address(KNOWN_ETHEREUM_ADDRESS):
            logging.debug(
                f"Recovered address: {recovered_address} "
                f"Expected address: {KNOWN_ETHEREUM_ADDRESS}"
            )
            print("Invalid signature.")
            return False

        print("Valid signature.")
        return True

    except Exception as e:
        logging.error("Invalid signature", e)
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
