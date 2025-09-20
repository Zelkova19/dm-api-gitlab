from datetime import datetime

import allure
from hamcrest import (
    assert_that,
    all_of,
    starts_with,
    has_property,
    has_properties,
    ends_with,
    instance_of,
    equal_to,
)


class PostV1Account:
    @classmethod
    def check_response_values(cls, response): # type: ignore[no-untyped-def]
        with allure.step("Проверка ответа"):
            today = datetime.now().strftime("%Y-%m-%d")
            assert_that(str(response.resource.registration), starts_with(today))
            assert_that(
                response,
                all_of(
                    has_property("resource", has_property("login", ends_with("Roman"))), # type: ignore[arg-type]
                    has_property( # type: ignore[arg-type]
                        "resource",
                        has_property("registration", instance_of(datetime)), # type: ignore[arg-type]
                    ),
                    has_property( # type: ignore[arg-type]
                        "resource",
                        has_properties(
                            {
                                "rating": has_properties(
                                    {
                                        "enabled": equal_to(True),
                                        "quality": equal_to(0),
                                        "quantity": equal_to(0),
                                    }
                                )
                            }
                        ),
                    ),
                ),
            )
