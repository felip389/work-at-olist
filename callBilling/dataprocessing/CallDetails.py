

class CallDetails:
    def __init__(self):
        self.valid = False
        self.invalid_msg = ''
        self.call_id = 0
        self.start = 0
        self.end = 0
        self.source = 0
        self.destination = 0
        self.call_price = 0

    def set_values(self, call_id, start, end, source, destination):
        self.call_id = call_id
        self.start = start
        self.end = end
        self.source = source
        self.destination = destination

    def get_call_id(self):
        return self.call_id

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_source(self):
        return self.source

    def get_destination(self):
        return self.destination

    def is_valid(self):
        return self.valid

    def set_valid(self):
        self.valid = True

    def set_invalid_msg(self, msg):
        self.invalid_msg = msg
        self.valid = False

    def get_invalid_msg(self):
        return self.invalid_msg

    def get_call_price(self):
        return self.call_price

    def set_call_price(self, price):
        self.call_price = price
