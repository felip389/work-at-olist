

class SignalResult:
    def __init__(self):
        self.msg = ''
        self.httpCode = 0
        self.valid = False

    def set_result(self, msg, httpcode, valid):
        self.msg = msg
        self.httpCode = httpcode
        self.valid = valid

    def get_msg(self):
        return self.msg

    def get_http_code(self):
        return self.httpCode

    def is_valid(self):
        return self.valid
