

class CallDetails:
    def __init__(self):
        self.call_id = 0
        self.start = 0
        self.end = 0
        self.source = 0
        self.destination = 0

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
