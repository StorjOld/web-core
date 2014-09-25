import requests
import json

def create(real_deal, base_url, key):
    """Create an account api interface

    If real_deal is False, this returns
    a fake api which always returns false.
    Use this if you wish to disable balance
    checks.

    """
    if real_deal:
        return AccountsApi(base_url, key)
    else:
        return FakeAccountsApi()


class Receipt(object):
    def __init__(self, token, amount):
        self.token = token
        self.amount = amount

class AccountsApi(object):
    def __init__(self, base_url, key):
        self.base_url = base_url
        self.key = key

    def consume(self, token, amount):
        response = requests.post(
                self.base_url + "/token/withdraw/" + token,
                headers=self.headers(),
                data=json.dumps({ 'bytes': amount }))

        if response.status_code == 200:
            return Receipt(token, amount)
        else:
            return None

    def deposit(self, token, amount):
        response = requests.post(
                self.base_url + "/token/deposit/" + token,
                headers=self.headers(),
                data=json.dumps({ 'bytes': amount }))

        if response.status_code == 200:
            return Receipt(token, amount)
        else:
            return None

    def refund(self, receipt):
        self.deposit(receipt.token, receipt.amount)

    def headers(self):
        return {
                'Authentication': self.key,
                'Content-Type': 'application/json'
                }


class FakeAccountsApi(object):
    def consume(self, token, amount):
        return True

    def deposit(self, token, amount):
        return True

    def refund(self, receipt):
        pass
