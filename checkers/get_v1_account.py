from datetime import datetime

import allure
import httpx
from hamcrest import (
    assert_that,
    has_property,
    ends_with,
    instance_of,
    has_properties,
    greater_than_or_equal_to,
    equal_to,
)


class GetV1Account:
    @classmethod
    def get_v1_account(cls, response: httpx.Response, login_suffix: str):  # type: ignore[no-untyped-def]
        with allure.step("Проверка ответа"):
            assert_that(
                response,
                has_property("resource", has_property("login", ends_with(login_suffix))),  # type: ignore[arg-type]
            )
            assert_that(response, has_property("resource", has_property("info", "")))  # type: ignore[arg-type]
            assert_that(
                response,
                has_property(
                    "resource",
                    has_property("registration", instance_of(datetime)),  # type: ignore[arg-type]
                ),
            )
            assert_that(
                response,
                has_property(
                    "resource",
                    has_properties(
                        {
                            "settings": has_properties(
                                {
                                    "paging": has_properties(
                                        {
                                            "posts_per_page": greater_than_or_equal_to(10),
                                            "comments_per_page": equal_to(10),
                                            "topics_per_page": equal_to(10),
                                            "messages_per_page": equal_to(10),
                                            "entities_per_page": equal_to(10),
                                        }
                                    )
                                }
                            )
                        }
                    ),
                ),
            )
