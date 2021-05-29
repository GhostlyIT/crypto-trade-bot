import hmac
import requests
from time import time
from urllib.parse import urlencode
from settings import settings


class BTCAlphaClient:
    @staticmethod
    def __generate_headers(data):
        msg = settings['exchange_api']['key'] + urlencode(sorted(data.items(), key=lambda val: val[0]))

        sign = hmac.new(settings['exchange_api']['secret'].encode(), msg.encode(), digestmod='sha256').hexdigest()

        return {
            'X-KEY': settings['exchange_api']['key'],
            'X-SIGN': sign,
            'X-NONCE': str(int(time() * 1000)),
        }

    def make_request(self, endpoint, method='get', data={}):
        return requests.request(method, settings['exchange_api']['base_url'] + '/' + endpoint,
                                headers=self.__generate_headers(data))

    def get_currencies(self):
        return self.make_request('currencies')

    def get_wallet_info(self, currency=''):
        return self.make_request('wallets?currency_id=' + currency)


