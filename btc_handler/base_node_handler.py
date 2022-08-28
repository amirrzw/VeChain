from decimal import Decimal
from typing import Optional, Union, Literal

from btc_handler.Providers.JsonRPCProvider import JsonRPCProvider
from btc_handler.api_switcher import APISwitcher

"""
    > Base Node Handler
    Basic functions for adding a new network to the TMWM
    => Raise your exceptions from the exceptions.py.
    => All the numbers should be Decimal (from the decimal library) type. Not int nor float [Except block heights and timestamps]
"""


class BaseNodeHandler:
    NETWORK_NAME = "ETH"
    NATIVE_TOKEN = {
        "token_symbol": "TRX",
        "token_standard": "TRC20",
        "network_name": NETWORK_NAME,
        "decimals": 6,
        "contract_address": None,
        "min_transfer_amount": 1,  # If this isn't set, the default got from the decimals field
        "identifier": 302301032,  # Just for the TRC10 on the TRX network or ..., so it is None for the other networks
    }

    API_SWITCHER_MODE = False  # Define if the handler use API Switcher or not
    # (Refer all your request functions to this parameter)
    PROVIDERS = {  # List of providers that the network can use them
        JsonRPCProvider.PROVIDER_NAME: JsonRPCProvider,
    }
    DEFAULT_PROVIDER = JsonRPCProvider.PROVIDER_NAME  # Default provider that network use most of the time

    API_SWITCHER_CLIENT = APISwitcher(network_name=NETWORK_NAME, providers=PROVIDERS, default_provider=DEFAULT_PROVIDER)
    # API Switcher client that can be used in your request functions

    @staticmethod
    def get_network_configuration() -> dict:
        """
        Returns basic information of the network
        @return: a dictionary in shape of bellow:
        {
            "network_name": "TRX",
            "min_confirmation": 3,
            "block_time": 5,  It should be in seconds
            "is_utxo_based": False,
            "support_balance_snapshot": False,
            "check_deposits_by_block": True,
            "support_canceling_transactions": False,
            "is_sequential": True,
            "address_regex": "\\w{64}",
            "memo_regex": "\\w{64}", If the network doesn't have a certain memo regex, leave it to None
            "coin_type_code": 60, Get it from https://github.com/satoshilabs/slips/blob/master/slip-0044.md
            "native_token": NATIVE_TOKEN Defined earlier
        }
        """
        raise NotImplementedError

    @staticmethod
    def is_smart_contract_address(address: str) -> bool:
        """
        Check an address that whether it is a smart contract address or not
        @param address: The address that wants to be checked
        @return: A boolean that defines that the address is a smart contract or not
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if the network doesn't support this function
        """
        raise NotImplementedError

    @staticmethod
    def is_checksum_valid(address: str) -> bool:
        """
        Check if an address has correct checksum or not
        @param address: an address in string format
        @return: if the given address has true checksum or not
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_all_tokens(symbols: list) -> dict:
        """
        Returns all available tokens in the blockchain filtered by symbols
        @param symbols: a list of symbols of desired currencies which we are searching for their token details
                        e.g. ["USDT", "PUNDIX", "BNB", ...]
                        (If the symbol doesn't exist on the network, skip it. Don't raise an exception)
        @return: a list of tokens in dictionary format of:
        [
            {
                "token_symbol": "USDT",
                "token_standard": "TRC20",
                "network_name": "TRX",
                "decimals": 8,
                "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
                "gas_limit": 2500  # just for networks that need gas_limit in their transactions
                "min_transfer_amount": 1,  # if this is not set, the default got from decimals field.
                "identifier": 12341232,  # just for TRC10 on TRX or ..., so it is None for others
            }, ...
        ]
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_last_block() -> int:
        """
        Returns last mined block height in this blockchain
        @return: height of last mined block
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_block_timestamp(block_number: int) -> int:
        """
        return timestamp of the given block_number in seconds
        @param block_number: the height of the block wanted e.g. 1234518132
        @return an integer representing the block mined time in milliseconds unit
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_balance(token: dict, addresses: list, until_block: Union[int, Literal["latest"]] = "latest"):
        """
        Returns balance of desired token for requested addresses
        @param token: The token which trying to get it's fee in dict format of:
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        @param addresses: list of addresses which their balance is requested
        @param until_block: number representing the block that we should return balances till that block
        @return: a dict with format of
        {
            "balances":
                    [
                        {
                            "address": hex1,
                            "sub_address": "asdfjlaskdnvi",
                            "balance": amount1
                        }, ...
                    ],
            "until_block": until_block
        }
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if network does not support min_confirmation and until_block is not "latest"
        @raise NotImplementedError: if token is not valid or token_standard not implemented yet
        """
        raise NotImplementedError

    @staticmethod
    def get_all_token_balances(tokens: list, addresses: list,
                               until_block: Union[int, Literal["latest"]] = "latest") -> dict:
        """
        Returns balance of desired token for requested addresses
        @param tokens: a list of dictionary of tokens in shape of
        [
            {
                "token_symbol": "USDT",
                "token_standard": "ERC20",
                "network_name": "ETH",
                "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
                "identifier": "1231723" # just for some networks and tokens
            }, ...
        ]
        @param addresses: list of addresses which their balance is requested
        @param until_block: number representing the block that we should return balances till that block
        @return: a dict with format of
        {
            "token_balances": [
                {
                    "token":
                    {
                        "token_symbol": "USDT",
                        "token_standard": "ERC20",
                        "network_name": "ETH",
                        "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                        "decimals": 6,
                        "identifier": "1231723" # just for some networks and tokens
                    },
                    "balances": [
                        {
                            "address": "addr1",
                            "sub_address": "asdfjlaskdnvi",
                            "balance": "balance1"
                        }, ...
                    ]
                }, ...
            ],
            "until_block": 1234523
        }
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if network does not support min_confirmation and until_block is not "latest"
        @raise NotImplementedError: if token is not valid or token_standard not implemented yet
        """
        raise NotImplementedError

    @staticmethod
    def get_network_fee(token: dict) -> dict:
        """
        Returns network fee for a transaction with one input and one output and solo
        input transaction fee and additional input and output
        @param token: The token which trying to get it's network_fee in dict format of:
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        @return: three decimals with unit of the native coin, first the network fee
        and second for fee for additional input in utxo based networks and third for additional output in a dictionary:
        {
            "default_fee": fee1,
            "additional_input_fee": fee2,
            "additional_output_fee": fee3
        }
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if token is not valid or token_standard not implemented yet
        """
        raise NotImplementedError

    @staticmethod
    def get_all_tokens_network_fees(tokens: list) -> list:
        """
        Returns network fee for a transaction with one input and one output and solo
        input transaction fee and additional input and output
        @param tokens: a list of dictionary of tokens in shape of
        [
            {
                "token_symbol": "USDT",
                "token_standard": "ERC20",
                "network_name": "ETH",
                "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
                "identifier": "1231723" # just for some networks and tokens
            }, ...
        ]
        @return: list of three decimals with unit of the native coin, first the network fee
        and second for fee for additional input in utxo based networks and third for additional
        output for each token in a dictionary like:
        [
            {
                "token": {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                },
                "default_fee": fee1,
                "additional_input_fee": fee2,
                "additional_output_fee": fee3
            }
        ]
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if token is not valid or token_standard not implemented yet
        """
        raise NotImplementedError

    @staticmethod
    def get_deposits_by_block(addresses: list, from_block: int, until_block: int, tokens: list) -> list:
        """
        Returns all deposits to given addresses in the given block window
        (same as get_deposits_by_time for block-based networks; raise NotImplementedError in other cases)
        @param addresses: a list of addresses in below format:
        [
            {
                "address": "asdfasdfewaf",
                "sub_address": "asdfwevwef",
            }, ...
        ]
        @param from_block: open lower bound of the block which we are looking deposits
        @param until_block: closed upper bound of the block which we are looking deposits
        @param tokens: tokens which we want to check their deposits in format of list of dicts:
        [
            {
                "token_symbol": "USDT",
                "token_standard": "ERC20",
                "network_name": "ETH",
                "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
                "identifier": "1231723" # just for some networks and tokens
            }, ...
        ]
        @return: a list of deposits in this format:
        [
            {
                "token": {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                },
                "from_address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                "to_address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                "txid": "0x30b8219b2a45a08644fa257dac59a56388fe97d0322637321ce28a6465fcf896",
                "amount": 0.0023,
                "block": 2134136,
                "fee": 0.00001,
                "param": 3,
                "memo": "1234",
            }, ...
        ]
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_deposits_by_time(addresses: list, from_time: int, until_time: int, tokens: list) -> list:
        """
        Returns all deposits to given addresses in the given block window
        (same as get_deposits_by_block for time-based networks; raise NotImplementedError in other cases)
        @param addresses: a list of addresses in below format:
        [
            {
                "address": "asdfasdfewaf",
                "sub_address": "asdfwevwef",
            }, ...
        ]
        @param from_time: closed lower bound of the time which we are looking deposits in milliseconds
        @param until_time: open upper bound of the time which we are looking deposits in milliseconds
        @param tokens: tokens which we want to check their deposits in format of list of dicts:
        [
            {
                "token_symbol": "USDT",
                "token_standard": "ERC20",
                "network_name": "ETH",
                "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
                "identifier": "1231723" # just for some networks and tokens
            }, ...
        ]
        @return: a list of deposits in this format:
        [
            {
                "token": {
                    "token_symbol": "USDT",
                    "token_standard": "ERC20",
                    "network_name": "ETH",
                    "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                    "decimals": 6,
                    "identifier": "1231723" # just for some networks and tokens
                },
                "from_address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                "to_address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                "txid": "0x30b8219b2a45a08644fa257dac59a56388fe97d0322637321ce28a6465fcf896",
                "amount": 0.0023,
                "block": 2134136,
                "fee": 0.00001,
                "param": 3,
                "memo": "1234",
            }, ...
        ]
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format or the network doesn't support this function at all
        """
        raise NotImplementedError

    @staticmethod
    def get_params(addresses: list) -> list:
        """
        Get params needed for creating transaction (nonce in ETH or sequence in BNB)
        of this network from it's nodeHandler
        @param addresses: a list of addresses in below format:
        [
            {
                "address": "asdfasdfewaf",
                "sub_address": "asdfwevwef",
            }, ...
        ]
        @return: a list with dictionaries of this format:
        [
            {
                "address": "address1",
                "param": 2
            }, ...
        ]
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise NotImplementedError: if the network does not have any parameter needed
            for sending transaction from an address
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
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise UTXOBasedNetworkError: Raise the proper exception from the UTXOBasedNetworkError family if the network
            is UTXO-based and something is wrong
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
    def get_contract_abi(contract_address: str) -> list:
        """
        Returns a dictionary with contract_addresses as keys and abi strings as value .If contract is a proxy we have
            to add contract_addresses and their abis of the contract.
        @param contract_address: Address of contract we want to get its abi
        @return: A dictionary with contract_addresses as keys and abis as their values. Result has to be like:
            [
               {
                   "contract_address": "0xjsflaskdjfiowaefajslf"
                   "abi": "{f: (a, b)}"
                   "is_main_contract": False
               },...
            ]
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't
            complete, in the wrong format
        @raise NotImplementedError: if the network doesn't support this function
        """
        raise NotImplementedError

    @staticmethod
    def broadcast_transaction(signed_transaction: str) -> dict:
        """
        Broadcasts a signed transaction to the blockchain
        @param signed_transaction: signed transaction in string form
        @return: a dict in format of
        {"is_successful": is_successful, "response": response_raw_string, "txid": hash,
        "error_message": "This transaction has not enough fuel!", "error": "FUEL_NOT_ENOUGH"}
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_transaction_info(txid: str, tokens: list, addresses: list = None) -> dict:
        """
        Returns all information of a transactions by its txid
        @param txid: the transaction id of desired transaction in form of string;
        e.g. 0x30b8219b2a45a08644fa257dac59a56388fe97d0322637321ce28a6465fcf896
        @param tokens: possible tokens that the transaction might be about
        @param addresses: a list of addresses that may be in the transaction output in form of:
        [
            {
                "address": "address_1",
                "sub_address": "sub_address_1"
            }, ...
        ]
        @return: a dictionary containing all information of the transaction in form of:
        {
            "txid": "0x30b8219b2a45a08644fa257dac59a56388fe97d0322637321ce28a6465fcf896",
            "token": {
                "token_symbol": "USDT",
                "token_standard": "ERC20",
                "network_name": "ETH",
                "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "decimals": 6,
                "identifier": "1231723" # just for some networks and tokens
            },
            "transaction_inputs": [
                {
                    "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                    "transaction_output_txid": "0x30b8219b2a45a08644fa257dac59a56388fe97d0322637321ce28a6465fcf896",
                    "param": 2
                }, ...
            ],
            "transaction_outputs": [
                {
                    "address": "0xaA9d27669558C8A1b4a4c5f3233C01E99cFfb99C",
                    "amount": 0.231,
                    "index": 1
                }, ...
            ],
            "total_amount": 3.0231,
            "timestamp", 1231834171,
            "block": 2134136,
            "fee": 0.00001,
            "memo": "1234",
        }
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise ContractFailException: raise this exception when the transaction is mined but some problem occurred that
            the transfer is not done correctly. This Exception is defined below. you should fill
            all the inputs of the initializer when raising it
        """
        raise NotImplementedError

    @staticmethod
    def get_block_by_transaction_id(txid: str) -> int:
        """
        Returns height of block by getting a transaction id
        @param txid: transaction id of transaction which trying to get it's block
        @return: height of block of transaction with id of txid
                 (Return Null if it doesn't exist)
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        @raise ContractFailException: raise this exception when the transaction is mined but some problem occurred that
            the transfer is not done correctly. This Exception is defined below. you should fill
            all the inputs of the initializer when raising it
        """
        raise NotImplementedError

    @staticmethod
    def get_fee_by_transaction_id(txid: list) -> Decimal:
        """
        Returns fee of transaction with id of txid
        @param txid: transaction id of transaction which trying to get it's fee
        @return: Exact fee of that transaction in Decimal format
                 (Return Null if it doesn't exist)
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError

    @staticmethod
    def get_received_amount_in_transaction(txid: str, addresses: list, token: dict) -> list:
        """
        Returns received amount of requested addresses in that specific transaction
        @param txid: id of requested transaction
        @param addresses: a list of addresses that may be in the transaction output in form of:
        [
            {
                "address": "address_1",
                "sub_address": "sub_address_1"
            },
            {
                "address": "address_1",
                "sub_address": "sub_address_1"
            }, ...
        ]
        @param token: The token which trying to create transaction of it in dict format of:
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        @return a list with this format:
        [
            {
                "address": address1,
                "received_amount": amount1
            }, ...
        ] (Return Null if it doesn't exist)
        @raise APIError: Raise the proper exception from the APIError family if something goes wrong from the API side
            rest_framework.exceptions.APIException with details of response.text and code of response.status_code
        @raise InvalidInputError: Raise the proper exception from the InvalidInputError family if the inputs aren't complete,
         in the wrong format
        """
        raise NotImplementedError
