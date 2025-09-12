import allure

from packages.rest_client.client import RestClient


class MailhogApi(RestClient):

    @allure.step("Получить все письма")
    async def get_api_v2_messages(
            self,
            limit=50
    ):
        """
        Get users email
        :return:
        """
        params = {
            'limit': limit
        }
        response = await self.get(
            path=f'/api/v2/messages',
            params=params
        )
        return response
