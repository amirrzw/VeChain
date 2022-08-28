from decimal import Decimal
from pprint import pprint

from btc_node_handler.btc.btc_address import BTC_ADDRESS_1
from btc_node_handler.btc_wallet.btc_private import BTC_PRIVATE_1, BTC_ADDRESS_2, BTC_PRIVATE_2
from btc_node_handler.btc_wallet.btc_tokens import BTC_TEST_TOKEN
from btc_node_handler.btc_wallet.btc_wallet import BTCWallet

if __name__ == "__main__":
    pass

    print("========== get_new_address_with_keys: ")
    pprint(BTCWallet.get_new_address_with_keys())

    print("========== form_transaction: ")
    formed_transaction = BTCWallet.form_transaction(
        transaction=
        {"inputs": [
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "address": BTC_ADDRESS_1,
                "param": 2,
            },
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "address": BTC_ADDRESS_2,
                "param": 3,
            }
        ],
            "outputs": [
                {
                    "address": BTC_ADDRESS_2,
                    "amount": Decimal(str(0.0001))
                }
            ],
            "fee": Decimal(str(0.1))
        },
        token=BTC_TEST_TOKEN
    )
    print(f"formed_transaction is {formed_transaction}")

    print("========== sign_transaction: ")
    signed_transaction = BTCWallet.sign_transaction(formed_transaction=formed_transaction["formed_transaction"],
                                                    accounts=[
                                                        {
                                                            "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                                            "param": 3,
                                                            "address": BTC_ADDRESS_1,
                                                            "private_key": BTC_PRIVATE_1
                                                        },
                                                        {
                                                            "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                                            "param": 3,
                                                            "address": BTC_ADDRESS_2,
                                                            "private_key": BTC_PRIVATE_2
                                                        }
                                                    ])
    pprint(signed_transaction)

    print("========== create_and_sign_transaction: ")
    trans = BTCWallet.create_and_sign_transaction(
        transaction=
        {"inputs": [
            {
                "address": BTC_ADDRESS_1,
                "private_key": BTC_PRIVATE_1,
                "param": 2,
            }
        ],
            "outputs": [
                {
                    "address": BTC_ADDRESS_2,
                    "amount": Decimal(str(0.0001)),
                }
            ],
            "fee": Decimal(str(0.1))
        },
        token=BTC_TEST_TOKEN
    )
    pprint(trans)
    signed_transaction = trans['signed_transaction']
