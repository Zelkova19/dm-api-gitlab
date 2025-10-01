from checkers.http_checkers import check_status_code_http
from dm_api_account.exceptions import ApiException
from helpers.account_helper import AccountHelper


async def test_delete_v1_account_login_auth(auth_account_helper: AccountHelper) -> None:
    with check_status_code_http():
        await auth_account_helper.dm_account_api.login_api.v1_account_login_delete(x_dm_auth_token="")


async def test_delete_v1_account_login_no_auth(account_helper: AccountHelper) -> None:
    with check_status_code_http(
        exception=ApiException,
        expected_status_code=401,
        expected_message="User must be authenticated",
    ):
        await account_helper.dm_account_api.login_api.v1_account_login_delete_with_http_info(x_dm_auth_token="")
