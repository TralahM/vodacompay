from datetime import datetime
import requests
import json
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
    ax = str(dt)
    return ax.split(".")[0].replace("-", "").replace(" ", "").replace(":", "")


def parse_async_result(content):
    root = etree.from_string(content)
    js_out = {}
    keys = []
    for dataItem in root.xpath("//dataItem"):
        name, t, value = dataItem.getchildren()
        keys.append({name.text: value.text})
    [js_out.update(ks) for ks in keys]
    return js_out


class Vodacash(object):
    def __init__(
        self,
        username,
        password,
        server_ip="167.71.65.114",
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
        conn = requests.post(
            self.LOGIN_URL, json={
                "Username": self.Username, "Password": self.Password}
        )
        result = json.loads(conn.content)
        self.token = result["token"]
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
                "command_id": self.C2B_CommandID,
                "callback_channel": self.Callback_Channel,
                "currency": currency,
                "language": self.Language,
                "initials": initials,
                "surname": surname,
            },
        ).content
        # print(result)
        result = json.loads(result)
        return result

    def b2c(self, customer_msisdn, amount, currency="CDF", *args, **kwargs):
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
                "command_id": self.B2C_CommandID,
                "callback_channel": self.Callback_Channel,
                "serviceprovidername": self.ServiceProviderName,
                "currency": currency,
                "language": self.Language,
            },
        ).content
        # print(result)
        result = json.loads(result)
        return result
