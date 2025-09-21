import allure

from tests.conftest import UserData
from helpers.account_helper import AccountHelper


@allure.suite("Проверка метода PUT V1/account.email")
class TestPutV1AccountEmail:
    @allure.title("Проверка смены почты")
    async def test_put_v1_account_email(self, account_helper: AccountHelper, prepare_user: UserData) -> None:
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        await account_helper.register_new_user(login=login, password=password, email=email)
        await account_helper.user_login(login=login, password=password)

        # Меняем email
        new_email = f"new_{login}@mail.ru"
        await account_helper.change_email(login=login, password=password, new_email=new_email)
        await account_helper.user_login(login=login, password=password)
