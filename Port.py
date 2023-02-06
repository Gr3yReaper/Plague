class Port:
    def __init__(self, country, destinations, activity):
        self.country = country
        self.destinations = destinations
        self.activity = activity

    def get_country(self):
        return self.country

    def get_destination(self):
        return self.destinations

    def get_activity(self):
        return self.activity

    def set_country(self, country):
        self.country = country

    def set_destinations(self, destinations):
        self.destinations = destinations

    def set_activity(self, activity):
        self.activity = activity
