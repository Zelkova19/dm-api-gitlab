import allure
import pytest

from faker import Faker
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from dm_api_account.exceptions import ApiException

from tests.conftest import UserData
from helpers.account_helper import AccountHelper

faker = Faker()


@allure.suite("Тесты на проверку метода POST V1/account")
class TestsPostV1Account:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка регистрации новго пользователя")
    async def test_post_v1_account(self, account_helper: AccountHelper, prepare_user: UserData) -> None:
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        await account_helper.register_new_user(login=login, password=password, email=email)
        response = await account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)

    @allure.sub_suite("Негативные тесты")
    @pytest.mark.parametrize(
        "title, login, email, password, status_code, error_message",
        [
            (
                "password",
                faker.name(),
                faker.email(),
                "12345",
                400,
                "Validation failed",
            ),
            (
                "email",
                faker.name(),
                "user.ru",
                faker.password(),
                400,
                "Validation failed",
            ),
            (
                "login",
                "U",
                faker.email(),
                faker.password(),
                400,
                "Validation failed",
            ),
        ],
    )
    async def test_post_v1_account_validation_filed(
        self,
        account_helper: AccountHelper,
        prepare_user: UserData,
        login: str,
        email: str,
        password: str,
        error_message: str,
        status_code: int,
        title: str,
    ) -> None:
        allure.dynamic.title(f"Валидация поля {title}")

        with check_status_code_http(
            exception=ApiException,
            expected_status_code=status_code,
            expected_message=error_message,
        ):
            await account_helper.register_new_user(login=login, password=password, email=email)
