import allure
import httpx

from packages.rest_client.client import RestClient


class MailhogApi(RestClient):
    @allure.step("Получить все письма")
    async def get_api_v2_messages(self, limit: int = 50) -> httpx.Response:
        """
        Get users email
        :return:
        """
        params = {"limit": limit}
        response = await self.get(path="/api/v2/messages", params=params)
        return response
