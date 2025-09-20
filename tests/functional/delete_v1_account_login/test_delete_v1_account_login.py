from checkers.http_checkers import check_status_code_http
from helpers.account_helper import AccountHelper


async def test_delete_v1_account_login_auth(auth_account_helper: AccountHelper) -> None:
    response = await auth_account_helper.dm_account_api.login_api.delete_v1_account_login()
    assert response.status_code == 204


async def test_delete_v1_account_login_no_auth(account_helper: AccountHelper) -> None:
    with check_status_code_http(401, "User must be authenticated"):
        await account_helper.dm_account_api.login_api.delete_v1_account_login()
