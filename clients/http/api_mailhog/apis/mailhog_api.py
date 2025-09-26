import allure
import httpx
from restcodegen.restclient.client import AsyncClient


class MailhogApi(AsyncClient):
    @allure.step("Получить все письма")
    async def get_api_v2_messages(self, limit: int = 50) -> httpx.Response:
        """
        Get users email
        :return:
        """
        params = {"limit": limit}
        response = await self.get(url="/api/v2/messages", params=params)
        return response
