from typing import Any, Union

import allure
import httpx

from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.user_details_envelope import (
    UserDetailsEnvelope,
)
from clients.http.dm_api_account.models.user_envelope import UserEnvelop
from packages.rest_client.client import RestClient


class AccountApi(RestClient):
    @allure.step("Регистрация нового пользователя")
    async def post_v1_account(self, registration: Registration) -> httpx.Response:
        """
        Register new user
        :param:
        :return:
        """
        response = await self.post(
            path="/v1/account",
            json=registration.model_dump(exclude_none=True, by_alias=True),
        )
        return response

    @allure.step("Запрос пользователя")
    async def get_v1_account(
        self, validate_response: bool = True, **kwargs: Any
    ) -> Union[httpx.Response, UserDetailsEnvelope]:
        """
        Get current user
        :return:
        """
        response = await self.get(path="/v1/account", **kwargs)
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step("Сброс пароля")
    async def post_v1_account_password(self, validate_response: bool = False, **kwargs: Any) -> httpx.Response:
        """
        Reset registered user password
        :return:
        """
        response = await self.post(path="/v1/account/password", **kwargs)
        if validate_response:
            UserEnvelop(**response.json())
        return response

    @allure.step("Изменения пароля")
    async def put_v1_account_password(self, **kwargs: Any) -> UserEnvelop:
        """
        Change registered user password
        :return:
        """
        response = await self.put(path="/v1/account/password", **kwargs)
        return UserEnvelop(**response.json())

    @allure.step("Активация пользователя")
    async def put_v1_account_token(
        self,
        user_token: str,
        validate_response: bool = True,
    ) -> Union[httpx.Response, UserEnvelop]:
        """
        Activate registered user
        :param validate_response:
        :param user_token:
        :return:
        """
        headers = {"accept": "test/plain"}
        response = await self.put(path=f"/v1/account/{user_token}", headers=headers)
        if validate_response:
            return UserEnvelop(**response.json())
        return response

    @allure.step("Смена почты")
    async def put_v1_account_email(
        self,
        json_data: Any,
        validate_response: bool = True,
    ) -> Union[httpx.Response, UserEnvelop]:
        """
        Change register user email
        :param validate_response:
        :param json_data:
        :return:
        """
        response = await self.put(path="/v1/account/email", json=json_data)
        if validate_response:
            return UserEnvelop(**response.json())
        return response
