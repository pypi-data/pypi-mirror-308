import subprocess
import sys

import pytest

from sympla_tools.tickets.signature.token import validate


@pytest.fixture
def message_and_signature():
    signature = "0x1e6912e765694db61b5291c94469ba339f1b7da3e921d5c3acd8ced279565053120e3e866c0158fe0eeddefdd113303adc1e56e79a9f1503386251786d4881f31b"

    message_json = '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"37884525610813"}'

    return message_json, signature


def test_validate_signature_success(message_and_signature):
    message_json, signature = message_and_signature

    assert validate(message_json, signature)


TEST_SIGNATURE = "0x1e6912e765694db61b5291c94469ba339f1b7da3e921d5c3acd8ced279565053120e3e866c0158fe0eeddefdd113303adc1e56e79a9f1503386251786d4881f31b"

TEST_JSON_MESSAGE = '{"address": "0x3e3857e99BE213aA914942C6482c33161Df51E16", "ItemTypeId": "37884525610813"}'


def test_validate_signature_main_module():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sympla_tools.tickets.signature.token",
            "validate",
            TEST_JSON_MESSAGE,
            TEST_SIGNATURE
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0, f"Error: {result.stderr}"

    assert (
        "Valid signature." in result.stdout
        or "Invalid signature." in result.stdout
    ), f"Invalid result: {result.stdout}"
