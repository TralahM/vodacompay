import pytest
import vodacash
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def Vodacash_obj():
    obj = vodacash.Vodacash(
        username="thirdpartyc2bw",
        password="thirdpartyc2bw",
        server_ip="64.225.75.98",
        b2c_code="15058",
        c2b_code="8337",
        c2b_command_id="InitTrans_oneForallC2B",
        b2c_command_id="InitTrans_one4allb2c",
        callback_channel="2",
        serviceprovidername="ONE4ALL",
        language="EN",
    )
    return obj


def test_vodacash_obtain_token(Vodacash_obj, printer):
    printer(Vodacash_obj.token)
    logger.debug(Vodacash_obj.token)
    Vodacash_obj.authenticate()
    assert Vodacash_obj.token is not None


def test_vodacash_c2b_transaction(Vodacash_obj, printer):
    result = Vodacash_obj.c2b(
        customer_msisdn="243814447581",
        amount="600",
        currency="CDF",
        initials="BMB",
        surname="BetModenge",
    )
    printer(result)
    logger.debug(result)
    assert isinstance(result, dict)


def test_vodacash_b2c_transaction(Vodacash_obj, printer):
    result = Vodacash_obj.b2c(
        customer_msisdn="243814447581", amount="700", currency="CDF",
    )
    printer(result)
    logger.debug(result)
    assert isinstance(result, dict)
