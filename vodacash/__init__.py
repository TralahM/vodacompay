from datetime import datetime
import requests
from lxml import etree

CallbackResponse = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<response>
<dataItem>
<name>ResponseCode<</name>
<type>String</type>
<value>200</value>
</dataItem>
</response>
"""


def strdate(dt):
    ax = str(dt)
    return ax.split('.')[0].replace('-', '').replace(' ', '').replace(':', '')


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
    def __init__(self, username, password, callback_url):
        self.LOGIN_URL = "http://167.71.65.114/api/v1/login"
        self.C2B_URL = "http://167.71.65.114/api/v1/c2b"
        self.Username = username
        self.Password = password
        self.token = None
        self.shortcode = None
        self.callback_channel = 2
        self.callback_url = callback_url
        self.authenticate()

    def authenticate(self):
        result = requests.post(
            self.LOGIN_URL, {"Username": self.Username, "Password": self.Password}).content
        self.token = result["token"]

    def c2b(self, customer_msisdn, amount):
        result = requests.post(
            self.C2B_URL,
            {
                "token": self.token,
                "CustomerMSISDN": customer_msisdn,
                "Amount": amount,
                "Date": strdate(datetime.utcnow()),
                "CallbackChannel": self.callback_channel,
                "CallbackURL": self.callback_url,
            }
        ).content
        return result
