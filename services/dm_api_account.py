from clients.http.dm_api_account.apis.account_api import AccountApi
from clients.http.dm_api_account.apis.login_api import LoginApi
from restcodegen.restclient.client import AsyncClient
from restcodegen.restclient.configuration import Configuration


class DMApiAccount:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.api_client = AsyncClient(configuration=self.configuration)
        self.login_api = LoginApi(self.api_client)
        self.account_api = AccountApi(self.api_client)
