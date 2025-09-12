from contextlib import contextmanager

import allure
import requests
import httpx
# from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = ''
        ):
    with allure.step("Проверка ответа"):
        try:
            yield
            if expected_status_code != requests.codes.OK:
                raise AssertionError(f'Ожидаемый статус код должен быть равен {expected_status_code}')
            if expected_message:
                raise AssertionError(f'Должно быть получено сообщение "{expected_message}", но запрос прошел успешно')
        except httpx.HTTPStatusError as e:
            assert e.response.status_code == expected_status_code
            assert e.response.json()['title'] == expected_message
