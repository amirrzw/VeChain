import requests

"""
    > API Switcher
    All the requests and API-Calls of the network should get through this class.
"""


class APISwitcher:
    def __init__(self, network_name: str, providers: dict, default_provider: str):
        """
        Initialize the API Switcher client. It should be done once per Node Handler.
        @param network_name: Name of the network
        @param providers: A dictionary that contains basic providers with their functions. Like this:
        {
            "json-rpc": JsonRPCProvider,
            ...
        }
        @param default_provider: Default provider which network mostly use
        """
        self.NETWORK_NAME = network_name
        self.PROVIDERS = providers
        self.DEFAULT_PROVIDER = default_provider

    def get_payload(self, function: str, **kwargs) -> list:
        """
        Returns the necessary data for making the request.
        Example: get_payload(function="balance", address="non239x8b2bi...")
        @param function: Name of the function
        @param kwargs: Needed parameters for the function
        @return: A list that contains providers with their payload
        """
        data = []
        function = f"get_{function}_request"
        for provider_name, provider in self.PROVIDERS.items():
            if hasattr(provider, function):
                payload = getattr(provider, function)(**kwargs)
                data.append({'provider': provider_name,
                             'payload': payload})
        return data

    def handle_request(self, payload: list, api_switcher_mode: bool = False, provider: str = None) -> tuple:
        """
        Handling the request and returns the response.
        @param payload: List of data that given from the get_payload
        @param api_switcher_mode: Whether the function use API Switcher or not
        @param provider: a specified provider to get payload from this provider instead of DEFAULT_PROVIDER
        @return: Response of the request
        """
        if api_switcher_mode:
            response = requests.post("api-switcher.com", json={"network": self.NETWORK_NAME,
                                                               "payloads": payload})
            response_data = response.json()['data']
            status_code = response.json()['status_code']
            provider_name = response.json()['provider_name']
        else:
            request = None
            if provider is None:
                provider = self.DEFAULT_PROVIDER
            for provider_payload in payload:
                if provider_payload['provider'] == provider:
                    request = provider_payload['payload']
                    break
            if request is not None:
                response = requests.request(url=request["base_url"] + request["path"],
                                            data=request["body"],
                                            headers=request["headers"],
                                            method=request["method"],
                                            params=request['params'])
                response_data = response.json()
                status_code = response.status_code
                provider_name = provider
            else:
                raise Exception("Default provider is not covered in payload")
        return response_data, status_code, provider_name

    def parse_response(self, function: str, response: dict, status_code: int, provider_name: str):
        """
        Parse the given response from the handle_request.
        @param function: The function that you called
        @param response: Given response dictionary
        @param status_code: Status code of the request
        @param provider_name: What provider did handle_request use
        @return: The parsed response that can be used in the Node Handler
        """
        provider = self.PROVIDERS[provider_name]
        function = f"parse_{function}_response"
        if hasattr(provider, function):
            parsed_response = getattr(provider, function)(response=response, status_code=status_code)
        else:
            raise Exception(f"{provider} has not function {function}")
        return parsed_response

    def request_providers(self, function, provider=None, **kwargs):
        """
        It uses the above functions to handle a request, parse it and return it to the Node Handler.
        @param function: The function that you want to call
        @param provider: a specified provider to get payload from this provider instead of DEFAULT_PROVIDER
        @param kwargs: Needed parameters for the function
        @return: The parsed response that can be used in the Node Handler
        """
        payload = self.get_payload(function=function, **kwargs)
        response_data, status_code, provider_name = self.handle_request(payload=payload, provider=provider)
        parsed_response = self.parse_response(function=function,
                                              response=response_data,
                                              status_code=status_code,
                                              provider_name=provider_name)
        return parsed_response
