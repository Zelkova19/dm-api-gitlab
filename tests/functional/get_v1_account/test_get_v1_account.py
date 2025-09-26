import allure
import httpx

from checkers.http_checkers import check_status_code_http
from checkers.get_v1_account import GetV1Account
from helpers.account_helper import AccountHelper


@allure.suite("Тесты на проверку метода GET V1/account")
class TestsGetV1Account:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Авторизованный запрос пользователя")
    async def test_get_v1_account_auth(self, auth_account_helper: AccountHelper) -> None:
        response = await auth_account_helper.dm_account_api.account_api.get_v1_account(x_dm_auth_token="")
        if isinstance(response, httpx.Response):
            GetV1Account.get_v1_account(response=response, login_suffix="Roman")

    @allure.sub_suite("Негативные тесты")
    @allure.title("Неавторизованный запрос пользователя")
    async def test_get_v1_account_no_auth(self, account_helper: AccountHelper) -> None:
        with check_status_code_http(
            expected_status_code=401,
            expected_message="User must be authenticated",
        ):
            await account_helper.dm_account_api.account_api.get_v1_account_with_http_info(x_dm_auth_token="")
