import allure

from tests.conftest import User
from helpers.account_helper import AccountHelper


@allure.suite("Проверка метода PUT V1/account.email")
class TestPutV1AccountEmail:
    @allure.title("Проверка семны почты")
    async def test_put_v1_account_email(self, account_helper: AccountHelper, prepare_user: User) -> None:
        login = prepare_user.login
        password = prepare_user.password  # type: ignore[attr-defined]
        email = prepare_user.email  # type: ignore[attr-defined]
        await account_helper.register_new_user(login=login, password=password, email=email)
        await account_helper.user_login(login=login, password=password)

        # Меняем email
        new_email = f"new_{login}@mail.ru"
        await account_helper.change_email(login=login, password=password, new_email=new_email)
        await account_helper.user_login(login=login, password=password)
