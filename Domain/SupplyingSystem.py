import requests
from log.Log import Log

class SupplyingSystem(object):

    # TODO: add logs!

    def __init__(self):
        self.addr = 'https://cs-bgu-wsep.herokuapp.com/'
        self.log = Log("", "")

    def supply_handshake(self):
        try:
            response = requests.post(self.addr, data={'action_type': 'handshake'})
            return response.text == 'OK'
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return False

    def supply(self, name, address, city, country, zip):
        try:
            response = requests.post(self.addr,
                                     data={'action_type': 'supply',
                                           'name': name,
                                           'address': address,
                                           'city': city,
                                           'country': country,
                                           'zip': zip})
            # print(response.text)
            # print(response.status_code)
            if response.status_code == 200:
                return int(response.text)
            return -1
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return -1

    def cancel_supply(self, transaction):
        try:
            response = requests.post(self.addr,
                                     data={'action_type': 'cancel_supply',
                                           'transaction_id': transaction})
            # print(response.text)
            return response.text == '1'
        except Exception as e:
            self.log.set_info('http connection failed', 'errorLog')
            print(e)
            return False


s = SupplyingSystem()
print(s.supply_handshake())
t = s.supply("asi asi", "Metzada 11", "Beer Sheva", "Israel", "889889")
print(t)
if t > 0:
    print(s.cancel_supply(t))

