import time
from json import JSONDecodeError, loads
from typing import Callable, Any, Optional

import allure
import httpx

from clients.http.dm_api_account.models.api_models import (
    LoginCredentials,
    Registration,
    UserEnvelope,
    ChangeEmail,
    ResetPassword,
    ChangePassword,
)
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
            self.dm_account_api.account_api.api_client.headers.update(token)
            self.dm_account_api.login_api.api_client.headers.update(token)
        else:
            raise ValueError("Response should be instance of httpx.Response")

    @allure.step("Смена пароля")
    async def change_password(self, login: str, email: str, password: str, new_password: str) -> None:
        user = await self.user_login(login=login, password=password, validate_response=False)
        if isinstance(user, httpx.Response):
            token = user.headers["x-dm-auth-token"]
        reset_password = {"login": login, "email": email}
        await self.dm_account_api.account_api.post_v1_account_password(
            reset_password=ResetPassword(**reset_password),
            headers={"x-dm-auth-token": token},
        )

        token = await self.get_token(login=login, token_type="reset")
        change_password = {
            "login": login,
            "oldPassword": password,
            "newPassword": new_password,
            "token": token,
        }

        await self.dm_account_api.account_api.put_v1_account_password(change_password=ChangePassword(**change_password))

    @allure.step("Регистрация нового пользователя")
    async def register_new_user(self, login: str, password: str, email: str) -> httpx.Response | UserEnvelope:
        registration = Registration(login=login, password=password, email=email)

        await self.dm_account_api.account_api.post_v1_account(registration=registration)
        start_time = time.time()
        token = await self.get_token(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, (
            f"Время получения токена превысило 3 секунды. Время выполнения {end_time - start_time}"
        )
        assert token is not None, "Ожидали токен, получили None"

        response = await self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @allure.step("Аутентификация пользователя")
    async def user_login(
        self,
        login: str,
        password: str,
        remember_me: bool = True,
        validate_response: bool = False,
        validate_headers: bool = False,
    ) -> httpx.Response | UserEnvelope:
        login_credentials = LoginCredentials(login=login, password=password, rememberMe=remember_me)
        if validate_response:
            response = await self.dm_account_api.login_api.post_v1_account_login_with_http_info(
                login_credentials=login_credentials
            )
            return response
        response = await self.dm_account_api.login_api.post_v1_account_login_with_http_info(
            login_credentials=login_credentials
        )
        if validate_headers and isinstance(response, httpx.Response):
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"

        return response

    @allure.step("Смена почты")
    async def change_email(
        self,
        login: str,
        password: str,
        new_email: str,
    ) -> httpx.Response | UserEnvelope:
        json_data = {"login": login, "password": password, "email": new_email}
        await self.dm_account_api.account_api.put_v1_account_email(change_email=ChangeEmail(**json_data))

        token = await self.get_token(login=login)
        assert token is not None, "Ожидали токен, получили None"
        response = await self.dm_account_api.account_api.put_v1_account_token(
            token=token,
        )
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
