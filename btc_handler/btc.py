from base_node_handler import BaseNodeHandler


class BTCHandler(BaseNodeHandler):

    @staticmethod
    def get_network_configuration():
        return 1

    @staticmethod
    def get_all_tokens(symbols):
        return 1

    @staticmethod
    def get_last_block():
        return 1

    @staticmethod
    def get_block_timestamp(block_number):
        return 1

    @staticmethod
    def get_balance(token, addresses, until_block="latest"):
        return 1

    @staticmethod
    def get_all_token_balances(tokens, addresses, until_block="latest"):
        return 1

    @staticmethod
    def get_network_fee(token):
        return 1

    @staticmethod
    def get_all_tokens_network_fees(tokens):
        return 1

    @staticmethod
    def get_deposits_by_block(addresses, from_block, until_block, tokens):
        return 1

    @staticmethod
    def get_deposits_by_time(addresses, from_time, until_time, tokens):
        return 1

    @staticmethod
    def get_params(addresses):
        return 1

    @staticmethod
    def form_transaction(transaction, token, memo=""):
        return 1

    @staticmethod
    def broadcast_transaction(signed_transaction):
        return 1

    @staticmethod
    def get_transaction_info(txid, tokens):
        return 1

    @staticmethod
    def get_block_by_transaction_id(txid):
        return 1

    @staticmethod
    def get_fee_by_transaction_id(txid):
        return 1

    @staticmethod
    def get_received_amount_in_transaction(txid, addresses, token):
        return 1
