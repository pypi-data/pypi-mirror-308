import subprocess
import sys

import pytest

from sympla_tools.tickets.signature.token import validate


@pytest.fixture
def valid_message_and_signature():
    signature = "0x35201bd1f94907519e1190bf5e1700a757a1f1991b7cef316010ad108da4249d13377a42250ab9c381cae96f32fd059842a7e6f85119a1dfb5c2d1e0fb61aa2e1c"

    message_json = '{"address":"0x7d9E7cFb0f07BFDd194e73Be8c695CE8310bB316","ItemTypeId":"TTLXK1YP81"}'

    return message_json, signature


@pytest.fixture
def invalid_message_and_signature():

    signature = "0x35201bd1f94907519e1190bf5e1700a757a1f1991b7cef316010ad108da4249d13377a42250ab9c381cae96f32fd059842a7e6f85119a1dfb5c2d1e0fb61aa2e1c"

    invalid_json = '{"address":"","ItemTypeId":"TTLXK1YP81"}'

    disordered_message_json = '{"ItemTypeId":"TTLXK1YP81","address":"0x7d9E7cFb0f07BFDd194e73Be8c695CE8310bB316"}'

    message_json_with_space = '{"address": "0x7d9E7cFb0f07BFDd194e73Be8c695CE8310bB316","ItemTypeId": "TTLXK1YP81"}'

    return (
        signature,
        invalid_json,
        disordered_message_json,
        message_json_with_space,
    )


def test_validate_invalid_signature(invalid_message_and_signature):
    signature, invalid_json, _, _ = invalid_message_and_signature

    validation = validate(invalid_json, signature)

    print(validation)

    assert validation is False


def test_validate_signature_success_disordered(invalid_message_and_signature):
    signature, _, disordered_message_json, _ = invalid_message_and_signature

    assert validate(disordered_message_json, signature)


def test_validate_signature_success_with_space(invalid_message_and_signature):
    signature, _, _, message_json_with_space = invalid_message_and_signature

    assert validate(message_json_with_space, signature)


def test_validate_signature_main_module(valid_message_and_signature):

    message_json, signature = valid_message_and_signature

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sympla_tools.tickets.signature.token",
            "validate",
            message_json,
            signature,
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


def test_validate_signature_success(valid_message_and_signature):
    message_json, signature = valid_message_and_signature

    assert validate(message_json, signature)
