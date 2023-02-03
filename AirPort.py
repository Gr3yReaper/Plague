class AirPort:
    def __init__(self, country, destinations, activity):
        self.country = country
        self.destinations = destinations
        self.activity = activity

    def get_country(self):
        return self.country

    def get_destinations(self):
        return self.destinations

    def get_activity(self):
        return self.activity

    def update_destinations(self, destinations):
        self.destinations = destinations

    def update_activity(self, activity):
        self.activity = activity
