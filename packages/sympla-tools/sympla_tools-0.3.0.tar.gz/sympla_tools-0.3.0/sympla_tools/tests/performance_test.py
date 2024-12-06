import concurrent.futures

import pytest

from sympla_tools.tickets.signature.ethereum_token import validate


@pytest.fixture
def single_test_case():
    return (
        '{"address":"0x7d9E7cFb0f07BFDd194e73Be8c695CE8310bB316","ItemTypeId":"TTLXK1YP81"}',
        "0x35201bd1f94907519e1190bf5e1700a757a1f1991b7cef316010ad108da4249d13377a42250ab9c381cae96f32fd059842a7e6f85119a1dfb5c2d1e0fb61aa2e1c",
    )


def validate_case(case):
    message_json, signature = case
    return validate(message_json, signature)


@pytest.fixture
def multiple_test_cases():
    return [
        (
            '{"address":"0x7d9E7cFb0f07BFDd194e73Be8c695CE8310bB316","ItemTypeId":"TTLXK1YP81"}',
            "0x35201bd1f94907519e1190bf5e1700a757a1f1991b7cef316010ad108da4249d13377a42250ab9c381cae96f32fd059842a7e6f85119a1dfb5c2d1e0fb61aa2e1c",
        ),
        (
            '{"address":"0x31780ba7fda7934923d8ffd5077315d30db4bf1b","ItemTypeId":"TTWC509CAA"}',
            "0xf078c4a1b1adfce4161e77bb6cb3e82cc6f116c881b0b0f93a135a6dd037d4c073bec213f41b5ae738b88ed8cef298b8da779c0400c09fbff287b48c549b318b1c",
        ),
        (
            '{"address":"0x31780ba7fda7934923d8ffd5077315d30db4bf1b","ItemTypeId":"TTWC509C95"}',
            "0xe0a945d842162ed1ba546109022252a88e046811ea36043f19e31e3580da2a2c1947831ecc149f15aa749b0360e5dc5ba557397413e812b74483613e7f4bdf7b1c",
        ),
        (
            '{"address":"0x31780ba7fda7934923d8ffd5077315d30db4bf1b","ItemTypeId":"TTWC1HLPQ4"}',
            "0xc52d52e88e23c4a7c3d41eef2e58dedd289f3d4ea351eb932f6e53aa0f414ec32ec181991d045e3a089b7ead9894d68a8f79a7d9500bcdffe0cfe3c986c1ecc61b",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"18180804235988"}',
            "0x0eb502df8b44996a5b8db40e06dd1883b65d8f8ea6f96a372995498035386f5650dde441efbe3e95e6281ecaabd8258a5d7a9e91b02451a86263a831b1511a831c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"60440519375514"}',
            "0xd74abb366face41413f26b41bc65655a3250081c685420c77c773a6977df01ce52c8e7613dfee10b152305ebba30abff084479ffedcabd0337f59bd60f7aebb11c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"17255764165369"}',
            "0x5980fcb08c69b334d589140a2c294ccf5dbc9351ec3829f3b3b23f1ba2652628035d6bd225e0f3bb0e3acc6f4ebd36318ce8841e1ce791c8b17eaee5a04d96ff1c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"34224168310707"}',
            "0x7932f43f66157508c18cdd8ba775ec2c57000697c11c780a5eb7527dd7d5672536d8411a63074cd3ab452c4f726a58cdcb8ce0f5896725fa34fb8a09f7ff59161c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"17873316993460"}',
            "0x1e69e15e13733643eaea01e4ebc1d2c72b27dc6c6d5c3212321d7f162bd107272daf6f26cc407975eedb97aa15c44deb244cb637295aafd21a78ee28d802c7011c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"63337493456923"}',
            "0xad466a51e00963da90a6cbcf1721f099f0916104ca1a84df55f8adfbd1b1583942c62d75d7a89e8c92ea5dcd6ff249d6c08a80128846dbf79a476ae32cc2ae421b",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"64184640178053"}',
            "0xf7ff809416cc80ab49ab0d7f98911c747316e4b7aad238d20981b0c7b05ccab644a8267f19ec06615371596a625d1026afc9d75359ef2fe4f566bd5693b845721c",
        ),
        (
            '{"address":"0x3e3857e99BE213aA914942C6482c33161Df51E16","ItemTypeId":"48873982622005"}',
            "0x635b90d80ea3888e70c957dddeeb3bbf5b431e2d200d65c7edca6a4bb928521e3ce4ff7217b237a4b284f870e924ace2a7a2065654411bb2a317f18f682334fa1b",
        ),
    ]


def test_performance_single_validation(benchmark, single_test_case):
    message_json, signature = single_test_case

    result = benchmark(validate, message_json, signature)
    assert result is True


def test_performance_multiple_validations(benchmark, multiple_test_cases):
    def multiple_validations():
        return [
            validate(message, signature)
            for message, signature in multiple_test_cases
        ]

    results = benchmark(multiple_validations)
    assert all(results)


def test_performance_multiple_validations_parallel(
    benchmark, multiple_test_cases
):
    def parallel_validations():
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = list(executor.map(validate_case, multiple_test_cases))
        return results

    results = benchmark(parallel_validations)
    assert all(results)
