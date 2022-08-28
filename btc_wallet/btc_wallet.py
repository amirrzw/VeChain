from btc_node_handler.btc_wallet.base_wallet import BaseWallet


class BTCWallet(BaseWallet):

    @staticmethod
    def get_new_address_with_keys():
        return 1

    @staticmethod
    def form_transaction(transaction, token, memo=""):
        return 1

    @staticmethod
    def sign_transaction(formed_transaction, accounts):
        return 1

    @staticmethod
    def create_and_sign_transaction(transaction, token, memo=""):
        return 1
