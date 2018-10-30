
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


class CameraIdentificationError(Exception):
    """When camera can not be identified
    ```code``` 500 = some error, 400 = unsupported camera
    """
    def __init__(self, message, code, inner_exception=None):
        self.message = message
        self.code = code
        self.inner_exception = inner_exception
        if inner_exception:
            self.message += ': ' + str(inner_exception)


class UnsupportedCameraError(CameraIdentificationError):
    def __init__(self):
        super().__init__('Unsupported Camera', 400)
