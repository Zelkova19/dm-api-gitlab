import allure

from tests.conftest import User
from helpers.account_helper import AccountHelper


@allure.suite("Проверка метода POST V1/account/token")
class TestsPostV1AccountToken:
    @allure.title("Проверка получения токена")
    async def test_post_v1_account_token(self, account_helper: AccountHelper, prepare_user: User) -> None:
        login = prepare_user.login
        password = prepare_user.password #type: ignore[attr-defined]
        email = prepare_user.email #type: ignore[attr-defined]
        await account_helper.register_new_user(login=login, password=password, email=email)
