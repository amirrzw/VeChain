from rest_framework.exceptions import APIException

"""
    > Exceptions
    Basic exceptions that you can use them to handle the common errors in your handlers
    => Any new exception out of this file should be checked with your supervisor.
"""


# > Super-Exceptions: Other exceptions are inherited from these. Don't raise them.


class BaseException(Exception):
    message = ""

    def __init__(self, message, message_fa=""):
        self.message = message
        self.message_fa = message_fa
        super().__init__(message)


class AbstractMethodError(Exception):
    def __init__(self, class_name):
        super().__init__(f"You can't instance the {class_name} directly")


class InvalidInputError(Exception):
    def __init__(self, message):
        if type(self) is InvalidInputError:
            raise AbstractMethodError(class_name="InvalidInputError")
        self.message = message
        super().__init__(message)


class UTXOBasedNetworkError(Exception):
    def __init__(self, message):
        if type(self) is UTXOBasedNetworkError:
            raise AbstractMethodError(class_name="UTXOBasedNetworkError")
        self.message = message
        super().__init__(message)


class APIError(APIException):  # APIException from rest_framework
    def __init__(self, error: str, node: str, status_code: int, message: str, **kwargs):
        if type(self) is APIError:
            raise AbstractMethodError(class_name="APIError")
        self.code = status_code
        self.node = node
        self.error = error
        self.detail = f'{message}, "{error}"'
        if kwargs:
            self.detail += f" => {kwargs}"
        super().__init__(detail=self.detail, code=self.code)


class TransactionExpiredException(BaseException):
    def __init__(self, message):
        super().__init__(message)



class ContractFailException(BaseException):
    def __init__(self, response, error_message, error, block, consumed_fee):
        """
        @param response: The exact response object that the node has returned
        @param error_message: The error message in English that explains the error
        @param error: Error specific keyword
        @param block: the block which the transaction is mined on
        @param consumed_fee: the fee that is spent
        """
        self.error = error
        self.response = response
        self.error_message = error_message
        self.block = block
        self.consumed_fee = consumed_fee
        super().__init__(error_message)

    def __str__(self):
        return f"A transaction is failed with is failed and registered in block {self.block}" \
               f"with fee of {self.consumed_fee} and response of {self.response}"


class BadAddressException(BaseException):
    def __init__(self, message):
        super(BadAddressException, self).__init__(message)


class MemoRegexException(BaseException):
    def __init__(self, message):
        super(MemoRegexException, self).__init__(message)


# > Node & Wallet Handler Exceptions: Use these exceptions for the handlers

class IncompleteInput(InvalidInputError):
    def __init__(self, missing: str, invalid_input: any, message="Input is not complete"):
        """This exception is used when the inputs of the function miss something
        @param missing: The variable that functions needs, but it's not in the input
        @param invalid_input: Whole input of the function
        """
        self.missing = missing
        self.input = input
        super().__init__({"message": message, "missing": missing, "invalid_input": invalid_input})


# class InvalidResource(InvalidInputError):
#     def __init__(self, resource: any, message="The Resource doesn't exist"):
#         """This exception is used when a specific input doesn't exist on the network
#         @param resource: The resource that doesn't exist on the network (It could be an address, a token, ...)
#         """
#         self.resource = resource
#         super().__init__({"message": message, "resource": resource})


class InvalidAddressError(InvalidInputError, BadAddressException):
    def __init__(self, address: str, regex: str, message="Address is invalid"):
        """This exception is used when the given address isn't valid
        (It could be because of the regex or just network tells us)
        @param address: The invalid address
        @param regex: The network address regex
        """
        self.address = address
        self.regex = regex
        super().__init__({"message": message, "address": address, "regex": regex})


class InvalidMemoError(InvalidInputError, MemoRegexException):
    def __init__(self, memo: str, regex: str, message="Memo is invalid"):
        """This exception is used when the given memo isn't valid with the network memo regex
        @param memo: The invalid memo
        @param regex: The network memo regex
        """
        self.memo = memo
        self.regex = regex
        super().__init__({"message": message, "memo": memo, "regex": regex})


class InvalidBlockError(InvalidInputError):
    def __init__(self, block: int, message: str = "Block is invalid"):
        """This exception is used when the given block is not valid
        @param block: The invalid block
        """
        self.block = block
        super().__init__({"message": message, "block": block})

class InvalidTxidError(InvalidInputError):
    def __init__(self, txid: str, message: str = "Txid is invalid"):
        """This exception is used when the given txid is not valid
        @param txid: The invalid txid
        """
        self.txid = txid
        super().__init__({"message": message, "txid": txid})


class InvalidTokenError(InvalidInputError):
    def __init__(self, token: dict, message: str = "Token is invalid"):
        """This exception is used when the token is not valid in the network
        @param token: The token in this format
        {
            "token_symbol": "USDT",
            "token_standard": "ERC20",
            "network_name": "ETH",
            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
            "decimals": 6,
            "identifier": "1231723" # just for some networks and tokens
        }
        """
        self.token = token
        super().__init__({"message": message, "token": token})


class InvalidChecksumError(InvalidInputError):
    def __init__(self, address: str, message: str = "Checksum of the address is invalid"):
        """This exception is used when the given address has a wrong checksum
        @param address: The given adderss
        """
        self.address = address
        super().__init__({"message": message, "address": address})


class InvalidContractAddress(InvalidInputError):
    def __init__(self, contract_address: str, message: str = "Contract Address is invalid"):
        """This exception is used when the given contract address is not valid
        @param contract_address: The invalid contract address
        """
        self.contract_address = contract_address
        super().__init__({"message": message, "contract_address": contract_address})


class InvalidABI(InvalidInputError):
    def __init__(self, contract_address: str, abi: str, supported_abis: list, message: str = "ABI is invalid"):
        """This exception is used when the contract address doesn't support this ABI
        @param contract_address: The contract address
        @param abi: The invalid abi
        @param supported_abis: A list of all supported abis for the contract address
        """
        self.contract_address = contract_address
        self.abi = abi
        super().__init__({"message": message, "contract_address": contract_address, "abi": abi,
                          "supported_abis": supported_abis})


class InvalidABIFunction(InvalidInputError):
    def __init__(self, contract_address, abi, function, supported_functions, valid_abi=None, message="ABI is invalid"):
        self.contract_address = contract_address
        self.abi = abi
        self.function = function
        self.supported_functions = supported_functions
        if valid_abi is not None:
            message += ", valid abi is " + valid_abi
        super().__init__({"message": message, "contract_address": contract_address, "abi": abi,
                          "function": function, "supported_functions": supported_functions})


class InvalidContractFunctionInput(InvalidInputError):
    def __init__(self, contract_address, abi, function, inputs, valid_inputs, message="ABI is invalid"):
        self.contract_address = contract_address
        self.abi = abi
        self.function = function
        self.inputs = inputs
        self.valid = valid_inputs
        super().__init__({"message": message, "contract_address": contract_address, "abi": abi, "function": function})


class RateLimit(APIError):
    def __init__(self, error: str, node: str, status_code: int, message: str = "API reached its limit"):
        """This exception is used when you reached the rate limit of the node
        @param error: The error that node gave you
        @param node: The node that you used
        @param status_code: The status code of the request
        """
        super().__init__(error=error, node=node, status_code=status_code, message=message)


class IPBan(APIError):
    def __init__(self, error: str, node: str, status_code: int,
                 message: str = "The IP has been banned from accessing the node"):
        """This exception is used when your IP has been banned from the node
        @param error: The error that node gave you
        @param node: The node that you used
        @param status_code: The status code of the request
        """
        super().__init__(error=error, node=node, status_code=status_code, message=message)


class BadRequest(APIError):
    def __init__(self, data: dict, error: str, node: str, status_code: int,
                 message: str = "The request is not valid"):
        """This exception is used when the request isn't valid.
        @param data: The request that you send to the node with its parameters, like this
        {
            "url": "https://blockfrost.com/...",
            "headers": {"project_id": "icowniwzdnoDW", ...}, Don't put API key in the dictionary!
            "body": {"address": "..."}
        }
        @param error: The error that node gave you
        @param node: The node that you used
        @param status_code: The status code of the request
        """
        super().__init__(error=error, node=node, status_code=status_code, message=message, data=data)


class MissingAPIKey(APIError):
    def __init__(self, error: str, node: str, status_code: int, message: str = "The request is not valid"):
        """This exception is used when the API key of the node is missing.
        @param error: The error that node gave you
        @param node: The node that you used
        @param status_code: The status code of the request
        """
        super().__init__(error=error, node=node, status_code=status_code, message=message)


class NetworkBusyException(BaseException):
    def __init__(self, network, main_exception_message, message=""):
        """This exception is used when the current network is unavailable.
        @param network: The network or the node that you used
        @param main_exception_message: The error that node gave you
        """
        self.message = f"Network {network} seems to be busy now."
        self.network = network
        self.main_exception_message = main_exception_message
        super(NetworkBusyException, self).__init__(message)

class BadBroadCastException(BaseException):
    def __init__(self, message):
        """This exception is used when something goes wrong while you were broadcasting the transaction
        @param message: The error that node gave you or the details of what happened
        """
        super(BadBroadCastException, self).__init__(message)


class TransactionInequality(UTXOBasedNetworkError):
    def __init__(self, input_amount: int, output: int,
                 transaction: dict, message: str = "The input amount is not equal to the output"):
        """This exception is used when the total input amount of the transaction isn't equal to the total output.
        @param input_amount: Total amount of the input
        @param output: Total amount of the output
        @param transaction: Full details of the transaction in dictionary format
        """
        self.input = input
        self.output = output
        self.transaction = transaction
        super().__init__({"message": message, "input_amount": input_amount, "output": output, "transaction": transaction})


class InvalidUtxo(UTXOBasedNetworkError):
    def __init__(self, input_transaction: dict, txid: str, transaction: dict, message: str):
        """This exception is used when an input of the transaction used before or it is expired
        @param input_transaction: A dictionary of the input with this format
        { "address": "0xjdiwnbzniweunwzw...",
          "txid": "nzoiwnnwizueub...",
          "param": 0
        }
        @param txid: Transaction ID
        @param transaction: Full details of the transaction in dictionary format
        @param message: Full details of what goes wrong
        """
        self.input_transaction = input_transaction
        self.txid = txid
        self.transaction = transaction
        super().__init__({"message": message, "input_transaction": input_transaction, "transaction": transaction})


class UnknownException(BaseException):
    def __init__(self, message: str):
        """This exception is used when something unusual happens. Give full details in the message parameter.
        @param message: Full details of what caused this error
        """
        super(UnknownException, self).__init__(message)
