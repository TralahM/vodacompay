"""Vodacash Module."""
import json
from datetime import datetime

import requests
from lxml import etree

C2BCallbackResponse = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>
<dataItem>
<name>ResponseCode<</name>
<type>String</type>
<value>200</value>
</dataItem>
</response>
"""
B2CCallbackResponse = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>
<dataItem>
<name>ResponseCode<</name>
<type>String</type>
<value>200</value>
</dataItem>
<dataItem>
<name>RESULT_CODE<</name>
<type>String</type>
<value>Received</value>
</dataItem>
</response>
"""


def strdate(dt):
    """Generate a str of 12 digits from a datetime object `dt`."""
    ax = str(dt)
    return ax.split(".")[0].replace("-", "").replace(" ", "").replace(":", "")


def parse_async_result(content):
    """Parse result.

    Takes XML string `content` and parses out the fields then returns a  JSON/DICT
    python dictionary with the data Items.

    .. note::
        FOR INTERNAL USE ONLY

    """
    root = etree.from_string(content)
    js_out = {}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: value.text})
    [js_out.update(ks) for ks in keys]
    return js_out


class Vodacash(object):
    """Create A Vodacash Object to be Used throughout your API Interaction.

    *Arguments*

        username:
            Username as provided by Vodacash Team

        password:
            Password as provided by Vodacash Team

        server_ip:
            Your whitelisted server IP,domain name where the intermediary server is deployed.

        b2c_code:
            Your B2C code as provided by Vodacom default="15058",

        c2b_code:
            Your C2B code as provided by Vodacom default="8337",

        c2b_command_id:
            Your C2B CommandID as provided default="InitTrans_oneForallC2B",

        b2c_command_id:
            Your B2C CommandID as provided default="InitTrans_one4allb2c",

        callback_channel:
            Your callback channel default="2" for http url

        serviceprovidername:
            Your Provided ServiceProviderName default="ONE4ALL",

        language:
            Your chosen language default="EN",

    """

    def __init__(
        self,
        username,
        password,
        server_ip="",
        b2c_code="15058",
        c2b_code="8337",
        c2b_command_id="InitTrans_oneForallC2B",
        b2c_command_id="InitTrans_one4allb2c",
        callback_channel="2",
        serviceprovidername="ONE4ALL",
        language="EN",
        *args,
        **kwargs,
    ):
        """Initialize object."""
        self.LOGIN_URL = f"http://{server_ip}/api/v1/login"
        self.C2B_URL = f"http://{server_ip}/api/v1/c2b"
        self.C2B_CB_URL = f"http://{server_ip}/api/v1/c2b_callback"
        self.B2C_URL = f"http://{server_ip}/api/v1/b2c"
        self.B2C_CB_URL = f"http://{server_ip}/api/v1/b2c_callback"
        self.Username = username
        self.Password = password
        self.C2B_CommandID = c2b_command_id
        self.ServiceProviderName = serviceprovidername
        self.B2C_CommandID = b2c_command_id
        self.token = None
        self.Language = language
        self.C2B_Number = c2b_code
        self.B2C_Number = b2c_code
        self.Callback_Channel = callback_channel
        self.authenticate()

    def authenticate(self):
        """Authenticate.

        Obtains and sets an authentication token by authenticating against the
        Vodacom UATG payment gateway.
        """
        conn = requests.post(
            self.LOGIN_URL, json={
                "Username": self.Username, "Password": self.Password}
        )
        try:
            result = json.loads(conn.content)
            self.token = result["token"]
            conn.connection.close()
        except json.decoder.JSONDecodeError:
            conn.connection.close()

    def c2b(
        self,
        customer_msisdn,
        amount,
        currency="CDF",
        initials="BMB",
        surname="BetModenge",
        *args,
        **kwargs,
    ):
        """Handle c2b.

        *Required Arguments*

            customer_msisdn:
                Customer PhoneNumber
            amount:
                Amount to transact

        *Optional arguments*
            client_callback_url: URL Where to receive json callback data.

            currency:
                The currency code default CDF
            initials:
                The Business Initials default BMB
            surname:
                The Business Surname default BetModenge

        And Returns a dict object like:

        .. code-block:: json

                {
                    "Amount": "100",
                    "CallBackChannel": "2",
                    "CallBackDestination": "http://XX.XXX.XX.XX/api/v1/c2b_callback",
                    "CommandId": "InitTrans_oneForallC2B",
                    "Currency": "CDF",
                    "CustomerMSISDN": "243800000000",
                    "Date": "20200727182755",
                    "Initials": "TMB",
                    "InsightReference": "AB7158AA732221F8E054002128FBA42E",
                    "Language": "EN",
                    "ResponseCode": "0",
                    "ServiceProviderCode": "8337",
                    "Surname": "Surname",
                    "ThirdPartyReference": "R20200727212755",
                    "code": "3",
                    "description": "Processed",
                    "detail": "Processed",
                    "event_id": "80049"
                }
        """
        self.authenticate()
        result = requests.post(
            self.C2B_URL,
            json={
                "Amount": amount,
                "CustomerMSISDN": customer_msisdn,
                "Date": strdate(datetime.utcnow()),
                "thirdpartyref": "R" + strdate(datetime.now()),
                # "thirdpartyref": "BMB_UAT",
                "serviceprovidercode": self.C2B_Number,
                "token": str(self.token),
                "callback_url": str(self.C2B_CB_URL),
                "client_callback_url": kwargs.get("client_callback_url"),
                "command_id": self.C2B_CommandID,
                "callback_channel": self.Callback_Channel,
                "currency": currency,
                "language": self.Language,
                "initials": initials,
                "surname": surname,
            },
        ).content
        print(result)
        try:
            result = json.loads(result)
            return result
        except json.decoder.JSONDecodeError:
            return {"error": "Payment Service Unavailable,try again later"}

    def b2c(self, customer_msisdn, amount, currency="CDF", *args, **kwargs):
        """Handle b2c.

        Takes:
            customer_msisdn:
                Customer PhoneNumber
            amount:
                Amount to transact
        Optional arguments:
            client_callback_url: URL Where to receive json callback data.
            currency:
                The currency code default CDF

        And Returns a dict object like:

        .. code-block:: json

                {
                    "Amount": "100",
                    "CallBackChannel": "2",
                    "CallBackDestination": "http://XX.XX.XX.XX/api/v1/b2c_callback",
                    "CommandID": "InitTrans_one4allb2c",
                    "Currency": "CDF",
                    "CustomerMSISDN": "243800000000",
                    "Insight_txid": "ilu6sebgpdrj68t2d9vqrd7c0gceelgs",
                    "Language": "EN",
                    "ResponseCode": "0",
                    "ServiceProviderName": "ONE4ALL",
                    "Shortcode": "15058",
                    "ThirdPartyReference": "R20200727212753",
                    "TransactionDateTime": "20200727182753",
                    "code": "3",
                    "description": "Processed",
                    "detail": "Processed",
                    "event_id": "12001"
                }

        """
        self.authenticate()
        result = requests.post(
            self.B2C_URL,
            json={
                "Amount": amount,
                "CustomerMSISDN": customer_msisdn,
                "Date": strdate(datetime.utcnow()),
                "thirdpartyref": "R" + strdate(datetime.now()),
                "shortcode": self.B2C_Number,
                "token": str(self.token),
                "callback_url": str(self.B2C_CB_URL),
                "client_callback_url": kwargs.get("client_callback_url"),
                "command_id": self.B2C_CommandID,
                "callback_channel": self.Callback_Channel,
                "serviceprovidername": self.ServiceProviderName,
                "currency": currency,
                "language": self.Language,
            },
        ).content
        print(result)
        try:
            result = json.loads(result)
            # print(result)
            return result
        except json.decoder.JSONDecodeError:
            return {"error": "Payment Service Unavailable,try again later"}
