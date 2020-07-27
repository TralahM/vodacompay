import vodacash
import logging
import json
from pprint import pprint

logger = logging.getLogger(__name__)


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


def test_vodacash_obtain_token():
    Vodacashobj = Vodacash_obj()
    print(Vodacashobj.token)
    tkn = Vodacashobj.token
    print(len(tkn), "is length of token", tkn)
    print("\n\n")
    logger.debug(Vodacashobj.token)
    Vodacashobj.authenticate()
    assert Vodacashobj.token is not None


def test_vodacash_c2b_transaction():
    result = Vodacash_obj().c2b(
        customer_msisdn="243815649058",
        amount="100",
        currency="CDF",
        initials="BMB",
        surname="BetModenge",
    )
    pprint(result)
    with open("c2b_result.json", "w") as fp:
        json.dump(result, fp)
    logger.debug(result)
    print("\n\n\n\n")
    assert isinstance(result, dict)


def test_vodacash_b2c_transaction():
    result = Vodacash_obj().b2c(
        customer_msisdn="243815649058", amount="100", currency="CDF",
    )
    pprint(result)
    print("\n\n\n\n")
    with open("b2c_result.json", "w") as fp:
        json.dump(result, fp)
    logger.debug(result)
    assert isinstance(result, dict)


if __name__ == "__main__":
    test_vodacash_obtain_token()
    test_vodacash_b2c_transaction()
    test_vodacash_c2b_transaction()
