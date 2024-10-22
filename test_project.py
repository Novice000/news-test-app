from project import check_q, check_date, check_page, check_country, check_category
import pytest


def test_check_q():
    assert check_q("") == None
    with pytest.raises(SystemExit):
        check_q("a  ")
    assert check_q("bitcoin") == "bitcoin"
    assert check_q("sports") == "sports"


def test_check_date():
    assert check_date("2024-06-07") == "2024-06-07"
    assert check_date("2024-06-07T12:02:06") == "2024-06-07T12:02:06"
    with pytest.raises(SystemExit):
        check_date("20-06-2007")
    with pytest.raises(SystemExit):
        check_date("2024-06-07T25:06;07")
    assert check_date("") == None


def test_check_num():
    assert check_page("2") == 2
    assert check_page("14") == 14
    with pytest.raises(SystemExit):
        check_page("tea")
    with pytest.raises(SystemExit):
        check_page("tea2")


def test_check_country():
    assert check_country("US") == "us"
    assert check_country("Gb") == "gb"
    assert check_country("") == None
    with pytest.raises(SystemExit):
        check_country("et")
    with pytest.raises(SystemExit):
        check_country("us,gb")
    with pytest.raises(SystemExit):
        check_country("United States of America")


def test_check_category():
    assert check_category("business") == "business"
    assert check_category("sports") == "sports"
    assert check_category("") == None
    with pytest.raises(SystemExit):
        check_category("football")
