from hamcrest import assert_that, equal_to
from crawler import Crawler


def test_phone_numbers_parser():
    assert_that(
        Crawler._parse('(8495)123-45-67  +74951234567'),
        equal_to({'84951234567', '84951234567'})
    )

    assert_that(
        Crawler._parse('4951234567 dsfsfds 4981234567'),
        equal_to({'84951234567', '84981234567'})
    )

    assert_that(
        Crawler._parse('1234567'),
        equal_to({'84951234567'})
    )

    assert_that(
        Crawler._parse('this is not a phone number 31415926'),
        equal_to(set())
    )

    assert_that(
        Crawler._parse('<div class="phone-number__number">8 495 137-77-67</div>'),
        equal_to({'84951377767'})
    )
