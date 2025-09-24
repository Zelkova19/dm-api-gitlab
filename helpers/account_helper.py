import time
from json import JSONDecodeError, loads
from typing import Callable, Any, Union, Optional

import allure
import httpx

from clients.http.dm_api_account.models.login_credentials import (
    LoginCredentials,
)
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.user_envelope import UserEnvelop
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(function: Callable[..., Any]) -> Callable[..., Any]:
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        token = None
        count = 0
        while token is None:
            token = await function(*args, **kwargs)
            count += 1
            print(f"Попыток получить токен = {count}!")
            if count == 5:
                raise AssertionError("Превышено количество попыток активационного токена!")
            if token:
                return token
            time.sleep(1)
        return None

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi) -> None:
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    @allure.step("Авторизация пользователя")
    async def auth_client(self, login: str, password: str) -> None:
        response = await self.user_login(login=login, password=password, validate_response=False)
        if isinstance(response, httpx.Response):
            token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
            self.dm_account_api.account_api.set_headers(token)
            self.dm_account_api.login_api.set_headers(token)
        else:
            raise ValueError("Response should be instance of httpx.Response")

    @allure.step("Смена пароля")
    async def change_password(self, login: str, email: str, password: str, new_password: str) -> None:
        user = await self.user_login(login=login, password=password, validate_response=False)
        if not isinstance(user, httpx.Response):
            raise ValueError("Login response should be instance of httpx.Response")
        await self.dm_account_api.account_api.post_v1_account_password(
            json={"login": login, "email": email},
            headers={"x-dm-auth-token": user.headers["x-dm-auth-token"]},
        )

        token = await self.get_token(login=login, token_type="reset")
        await self.dm_account_api.account_api.put_v1_account_password(
            json={
                "login": login,
                "oldPassword": password,
                "newPassword": new_password,
                "token": token,
            }
        )

    @allure.step("Регистрация нового пользователя")
    async def register_new_user(self, login: str, password: str, email: str) -> httpx.Response:
        registration = Registration(login=login, password=password, email=email)

        await self.dm_account_api.account_api.post_v1_account(registration=registration)
        start_time = time.time()
        token = await self.get_token(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, (
            f"Время получения токена превысило 3 секунды. Время выполнения {end_time - start_time}"
        )
        assert token is not None, "Ожидали токен, получили None"

        response = await self.dm_account_api.account_api.put_v1_account_token(user_token=token, validate_response=False)

        if not isinstance(response, httpx.Response):
            raise ValueError("Login response should be instance of httpx.Response")

        return response

    @allure.step("Аутентификация пользователя")
    async def user_login(
        self,
        login: str,
        password: str,
        remember_me: bool = True,
        validate_response: bool = False,
        validate_headers: bool = False,
    ) -> Union[httpx.Response, UserEnvelop]:
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = await self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response,
        )
        if validate_headers and isinstance(response, httpx.Response):
            assert "x-dm-auth-token" != None, "Токен для пользователя не был получен"
        return response

    @allure.step("Смена почты")
    async def change_email(
        self, login: str, password: str, new_email: str, validate_response: bool = False
    ) -> httpx.Response | UserEnvelop:
        json_data = {"login": login, "password": password, "email": new_email}
        await self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)

        token = await self.get_token(login=login)
        assert token is not None, "Ожидали токен, получили None"
        response = await self.dm_account_api.account_api.put_v1_account_token(
            user_token=token, validate_response=validate_response
        )
        if not isinstance(response, httpx.Response):
            raise ValueError("Login response should be instance of httpx.Response")
        return response

    @retrier
    async def get_token(self, login: str, token_type: str = "activation") -> Optional[str]:
        token = None
        response = await self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()["items"]:
            try:
                user_data = loads(item["Content"]["Body"])
            except (JSONDecodeError, KeyError):
                continue

            user_login = user_data["Login"]
            activation_token = user_data.get("ConfirmationLinkUrl")
            reset_token = user_data.get("ConfirmationLinkUri")
            if user_login == login and activation_token and token_type == "activation":
                token = activation_token.split("/")[-1]
            elif user_login == login and reset_token and token_type == "reset":
                token = reset_token.split("/")[-1]

        return token
