import hmac
import requests
from time import time
from urllib.parse import urlencode
from settings import settings


class BTCAlphaClient:
    def __generate_headers(self, data: dict) -> dict:
        msg = settings['exchange_api']['key'] + urlencode(sorted(data.items(), key=lambda val: val[0]))

        sign = hmac.new(settings['exchange_api']['secret'].encode(), msg.encode(), digestmod='sha256').hexdigest()

        return {
            'X-KEY': settings['exchange_api']['key'],
            'X-SIGN': sign,
            'X-NONCE': str(int(time() * 1000)),
        }

    def __make_request(self, endpoint: str, method: str = 'get', data: dict = {}, params: dict = {}):
        return requests.request(method=method,
                                url=settings['exchange_api']['base_url'] + '/' + endpoint,
                                headers=self.__generate_headers(data=data),
                                params=params,
                                data=data)

    def get_currencies(self):
        return self.__make_request('currencies')

    def get_wallet_info(self, currency: str = ''):
        return self.__make_request(endpoint='wallets', params={'currency_id': currency})

    def get_created_orders(self, order_type: str = '', pair: str = '', status: str = '', limit: str = ''):
        params = {
            'type': order_type,
            'pair': pair,
            'status': status,
            'limit': limit
        }
        return self.__make_request(endpoint='orders/own', params=params)

    def get_order_info(self, order_id: int):
        return self.__make_request(endpoint='order/' + str(order_id))

    def create_order(self, order_type: str, pair: str, amount: float, price: float):
        order = {
            'type': order_type,
            'pair': pair,
            'amount': str(amount),
            'price': str(price)
        }

        return self.__make_request(endpoint='order/', method='post', data=order)

    def cancel_order(self, order_id: int):
        return self.__make_request(method='POST', endpoint='order-cancel', data={'order': order_id})

    def get_own_exchanges(self,
                          order_type: str = '',
                          pair: str = '',
                          limit: int = 100,
                          offset: int = 0,
                          ordering: str = '-id'):
        params = {
            'type': order_type,
            'pair': pair,
            'limit': limit,
            'offset': offset,
            'ordering': ordering
        }
        return self.__make_request(endpoint='exchanges/own', params=params)

    def get_charts(self, pair: str, timeline: str, limit: int = 720, since: int = None, until: int = None):
        params = {
            'limit': limit,
            'since': since,
            'until': until
        }

        return requests.get('https://btc-alpha.com/api/charts/' + pair + '/' + timeline + '/chart', params=params)
