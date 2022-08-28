
"""
    > Base Wallet Handler
    Basic functions for working with network wallet
    => Raise your exceptions from the exceptions.py.
    => You can't use any endpoint in these functions (except form_transaction). Everything should be done offline.
"""
from typing import Optional


class BaseWallet:
    @staticmethod
    def get_new_address_with_keys() -> tuple:
        """
        Use this function to create new address and get its private key and public key
        @return: a tuple: (address, public_key, private_key)
        @note: public_key must be compressed, means start with 02 or 03 (like 0330b07dc8ada9a8ca72d036dd23f181bb372c2fa8c1bc47cf927579ed345a294e)
                [https://www.oreilly.com/library/view/programming-bitcoin/9781492031482/ch04.html]
        @note: You should NOT USE any endpoint or library to implement this method!
        """
        raise NotImplementedError

    @staticmethod
    def derive_address_from_public_key(public_key: str) -> str:
        """
        Use this function to build the address of a public_key (compressed format, means start with 02 or 03) for a specific network
        @return: a tuple: (address)
        @note: You should NOT USE any endpoint or library to implement this method!
        """
        raise NotImplementedError

    @staticmethod
    def derive_address_from_private_key(private_key: str) -> str:
        """
        Use this function to build the address of a private key for a specific network
        @return: a str (address)
        @note: You should NOT USE any endpoint or library to implement this method!
        @note: private_key must be hex
        """
        raise NotImplementedError

    @staticmethod
    def form_transaction(transaction: dict, token: dict, memo: str = "") -> dict:
        """
        Form a transaction in given format
        @param token: The token which trying to form transaction of it in dict format of:
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        @param transaction: transaction in format of
        {   "inputs": [
                        {
                            "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                            "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                            "param": 3
                         },
                         {
                            "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                            "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                            "param": 4
                         },
                    ],
            "outputs": [
                        {
                            "address": addr1,
                            "amount":amount1
                        }, ...
                       ],
            "fee": fee
        }
        @param memo: e.g. "1234"
        @return: A dictionary that contains anything that signing functions need to have.
        Pay attention that the formed_transaction value is a string. You could dump the dictionary with json.dumps()
        {
            "formed_transaction": "
            {
                'raw_transaction': 'eb250b07f2ea74d578f703f5955fd948b7afd61477118d17122c327ae7daa782',
                'message_hash': [
                    {
                        'address': '0x9C9cce02e73Eb39845F7056F85D7a3B31b00c307',
                        'public_key': '03aef4f7f68e02fac2b19734985fb2a6c67a8eef744b79036ba82bb92d29f12c0f',
                        'message_hash': '...'
                    }, ...
                ]
            }
            ",
            "fee" : 0.23
        }
        @raise NotImplementedError: if transaction is not in your desired form for example the network is not UTXO-based
            and number of inputs or outputs are more than one,
            or token is not valid or token_standard not implemented yet
        """
        raise NotImplementedError

    @staticmethod
    def form_transaction_v2(
            function: str,
            contract_address: str,
            contract_abi: Optional[str] = None,
            **kwargs,
    ) -> dict:
        """
        Form a transaction in given format
        @param contract_address: Contract address we want to call one of its functions in string format
                                 (if you want native or network token it should be NATIVE_TOKEN)
        @param contract_abi: Abi of the contract in string format
        @param function: Name of the function we are going to call in string format
        @param kwargs: Inputs of the function we are going to call
        NOTE: if contract_address and contract_abi are None at the same time, and function is transfer,
                you should transfer the native token of the blockchain
        @return: A string of the formed transaction that can be parsed and used in sign_transaction function and the fee
            in format of bellow dictionary:
            {
                "formed_transaction": formed_transaction in hex format,
                "fee" : Decimal value of fee of this call,
            }
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't
            complete, in the wrong format
        @raise UTXOBasedNetworkError: Raise the proper exception from the UTXOBasedNetworkError family if the network
            is UTXO-based and something is wrong
        """
        raise NotImplementedError

    @staticmethod
    def sign_transaction(formed_transaction: str, accounts: list, transaction_params: dict) -> dict:
        """
        Sign a formed transaction by function form_transaction
        @note: This function could be combination of get_signatures and get_signed_transaction
        @note: You should check the raw_transaction with the transaction and token dictionary in case of manipulation
        @param transaction_params: transaction in format of
        {   "version": 1,
            "transaction":
                {   "inputs": [
                                {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                                    "param": 3
                                 },
                                 {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                                    "param": 4
                                 },
                            ],
                    "outputs": [
                                {
                                    "address": addr1,
                                    "amount":amount1
                                }, ...
                               ],
                    "fee": fee
                },
            "token":
                {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                }
        }
        @param formed_transaction: a transaction formed by form_transaction in string format.
        note that you may need to parse the string to dictionary or other formats.
        @param accounts: a list of all addresses and their private_key used in the transaction:
        [
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "param": 3,
                "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                "private_key": "asdasdfinevajfnh...",
            }, ...
        ]
        @return: dictionary in format of
        {"txid": txid, "signed_transaction": signed_transaction_string}
        @raise TransactionMismatch: Raise this exception when you try to match the transaction dictionary with the formed_transaciton
                                    but, they didn't match
        @raise SigningException: If something went wrong during the signing process
        """
        raise NotImplementedError

    @staticmethod
    def get_signatures(raw_transaction: str, accounts: dict, transaction_params: dict) -> list:
        """
        Gets the hex form of raw transaction and accounts private-keys and returns a dictionary of account signatures
        @note: You should check the raw_transaction with the transaction and token dictionary in case of manipulation
        @param transaction_params: transaction in format of
        {   "version": 1,
            "transaction":
                {   "inputs": [
                                {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                                    "param": 3
                                 },
                                 {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                                    "param": 4
                                 },
                            ],
                    "outputs": [
                                {
                                    "address": addr1,
                                    "amount":amount1
                                }, ...
                               ],
                    "fee": fee
                },
            "token":
                {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                }
        }
        @param raw_transaction: Formed transaction in hex format (string) that needs to be signed
                                (returned from form_transaction and form_transaction_v2 functions)
        @param accounts: a list of all addresses and their private and public keys used in the transaction:
        [
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "param": 3,
                "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                "private_key": "asdasdfinevajfnh...",
                "public_key": "fniewnidcwiozwei..."
            }, ...
        ]
        @return: A list of dictionaries in bellow format:
        [
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "param": 3,
                "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                "signature": "asdasdfinevajfnh"
            }, ...
        ]
        @raise TransactionMismatch: Raise this exception when you try to match the transaction dictionary with the formed_transaciton
                                    but, they didn't match
        @raise SigningException: If something went wrong during the signing process
        """
        raise NotImplementedError

    @staticmethod
    def get_signed_transaction(raw_transaction: str, signatures: list, transaction_params: dict) -> dict:
        """
        Gets the hex form of the raw transaction and accounts signatures and returns the signed_transaction to broadcast
        @note: You should check the raw_transaction with the transaction and token dictionary in case of manipulation
        @param transaction_params: transaction in format of
        {   "version": 1,
            "transaction":
                {   "inputs": [
                                {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                                    "param": 3
                                 },
                                 {
                                    "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                                    "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                                    "param": 4
                                 },
                            ],
                    "outputs": [
                                {
                                    "address": addr1,
                                    "amount":amount1
                                }, ...
                               ],
                    "fee": fee
                },
            "token":
                {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                }
        }
        @param raw_transaction: Formed transaction in hex format (str) that needs to be signed
                                (returned from form_transaction and form_transaction_v2 functions)
        @param signatures: A list of dictionaries in bellow format:
        [
            {
                "transaction_output_txid": "0xaadadsfaadfasdfasd9adsaf323558C8A1b4adadfe",
                "param": 3,
                "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                "signature": "asdasdfinevajfnh"
            }, ...
        ]
        @return: dictionary in format of
        {"txid": txid, "signed_transaction": signed_transaction_string}
        @raise TransactionMismatch: Raise this exception when you try to match the transaction dictionary with the formed_transaciton
                                    but, they didn't match
        @raise SigningException: If something went wrong during the signing process
        """
        raise NotImplementedError

    @staticmethod
    def create_and_sign_transaction(transaction: dict, token: dict, memo="") -> dict:
        """
        Create a transaction and sign it.
        Note that you could use the two function form_transaction and sign_transaction int this function.
        @param token: The token which trying to create transaction of it in dict format of:
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        @param transaction: transaction in format of
        {   "inputs": [
                        {
                            "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                            "transaction_output_txid": "",
                            "param": 3,
                            "private_key": "asdasdfinevajfnh"
                         },
                         {
                            "address": "0xaA9d27669558faA1b4a4c5f3233C01E99cFfb99C",
                            "transaction_output_txid": "",
                            "param": 4,
                            "private_key": "asdasdfinevajfnh"
                         },
                    ],
            "outputs": [
                        {
                            "address": addr1,
                            "amount":amount1
                        }, ...
                       ],
            "fee": fee
        }
        @param memo: e.g. "1234"
        @return: dictionary in format of
        {"txid": txid, "fee": fee, "signed_transaction": signed_transaction_string}
        @raise TransactionMismatch: Raise this exception when you try to match the transaction dictionary with the formed_transaciton
                                    but, they didn't match
        @raise SigningException: If something went wrong during the signing process
        """
        raise NotImplementedError

