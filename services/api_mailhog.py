from restcodegen.restclient.configuration import Configuration
from clients.http.api_mailhog.apis.mailhog_api import MailhogApi


class MailHogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        # self.api_client = AsyncClient(configuration=self.configuration)

        self.mailhog_api = MailhogApi(self.configuration)
