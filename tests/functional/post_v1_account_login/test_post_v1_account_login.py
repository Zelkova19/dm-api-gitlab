import allure

from tests.conftest import User
from helpers.account_helper import AccountHelper


@allure.suite("Проверка метода POST V1/account/login")
class TestPostV1AccountLogin:
    @allure.title("Аутентификация с пользователя")
    async def test_post_v1_account_login(self, account_helper: AccountHelper, prepare_user: User) -> None:
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        await account_helper.register_new_user(login=login, password=password, email=email)
        await account_helper.user_login(login=login, password=password)
