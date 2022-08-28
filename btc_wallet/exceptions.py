class TransactionMismatch(BaseException):
    def __init__(self, transaction: dict, token: dict, raw_transaction: str,  message: str = "Token is invalid"):
        """This exception is used when the transaction and token doesn't match the raw_transaction
        @param transaction: The token dictionary
        @param token: The token dictionary
        @param raw_transaction: The token dictionary
        """
        self.transaction = transaction
        self.token = token
        self.raw_transaction = raw_transaction
        super().__init__(message)


class SigningException(BaseException):
    def __init__(self, message: str = "Signing process went wrong"):
        """This exception is used when the signing process went wrong (Bytewise or ...)
        """
        self.message = message
        super().__init__(message)