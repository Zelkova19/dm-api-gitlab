import allure

from tests.conftest import User
from helpers.account_helper import AccountHelper


@allure.suite("Проверка метода POST V1/account/password")
class TestsPostV1AccountPassword:
    @allure.title("Проверка смены пароля")
    async def test_post_v1_account_password(self, account_helper: AccountHelper, prepare_user: User) -> None:
        login = prepare_user.login
        password = prepare_user.password  # type: ignore[attr-defined]
        email = prepare_user.email  # type: ignore[attr-defined]
        new_password = "011235813"
        await account_helper.register_new_user(login=login, password=password, email=email)
        await account_helper.user_login(login=login, password=password)
        await account_helper.change_password(
            login=login,
            email=email,
            password=password,
            new_password=new_password,
        )
        await account_helper.user_login(login=login, password=new_password)
