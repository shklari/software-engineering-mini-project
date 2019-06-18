import requests


class CollectingSystem(object):

    # TODO: add logs!

    def __init__(self):
        self.addr = 'https://cs-bgu-wsep.herokuapp.com/'

    def collect_handshake(self):
        try:
            response = requests.post(self.addr, data={'action_type': 'handshake'})
            return response.text == 'OK'
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return False

    def pay(self, card_number, month, year, holder, ccv, id):
        try:
            response = requests.post(self.addr,
                                     data={'action_type': 'pay',
                                             'card_number': card_number,
                                             'month': month,
                                             'year': year,
                                             'holder': holder,
                                             'ccv': ccv,
                                             'id': id})
            if response.status_code == 200:
                return int(response.text)
            return -1
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return -1

    def cancel_pay(self, transaction):
        try:
            response = requests.post(self.addr,
                                     data={'action_type': 'cancel_pay',
                                           'transaction_id': transaction})
            return response.text == '1'
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return False

