
class HttpError(Exception):
    def __init__(self, url, status, reason, response=None):
        self.url = url
        self.status = status
        self.reason = reason
        self.response = response
        self.message = "HTTP: {0} - {1}".format(self.status, self.reason)


class GoProConnectionError(Exception):
    def __init__(self, message, inner_exception=None):
        self.message = message
        self.inner_exception = inner_exception


class GoProError(HttpError):
    def __init__(self, url, status, reason, response):
        super().__init__(url, status, reason, response)
        self.error_code = response['error_code']
        self.error_msg = response['error_msg']
        self.message = "GoPro Error"


class GoProBusyError(Exception):
    def __init__(self):
        self.message = "Operation invalid while busy"
