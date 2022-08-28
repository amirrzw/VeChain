class JsonRPCProvider:
    PROVIDER_NAME = "JSON-RPC"
    BASE_URL = "172.24.2.3"

    @staticmethod
    def get_balance_request(address):
        return {
            "base_url": JsonRPCProvider.BASE_URL,
            "method": "POST",
            "headers": {},
            "body": {},
            "params": {},
            "path": "",
        }

    @staticmethod
    def parse_balance_response(response, status_code):
        return response["address"]
