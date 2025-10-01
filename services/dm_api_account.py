from dm_api_account import Configuration, ApiClient
from dm_api_account.api import AccountApi, LoginApi


class DMApiAccount:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.api_client = ApiClient(configuration=self.configuration)
        self.login_api = LoginApi(self.api_client)
        self.account_api = AccountApi(self.api_client)
