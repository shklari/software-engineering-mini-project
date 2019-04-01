

# interface
class ProcurementPolicy(object):

    def __init__(self):
        self.allowedCountries = []

    def add_country(self, new_country):
        self.allowedCountries.append(new_country)
