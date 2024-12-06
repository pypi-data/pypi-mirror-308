# 基本异常
class SpiderException(Exception):
    def __init__(self):
        super().__init__()

# 请求异常
class RequestException(SpiderException):
    def __init__(self, status_code: int, url: str):
        self.status_code = status_code
        self.url = url
        super().__init__()

    def __str__(self):
        return f'请求错误! url {self.url} status code {self.status_code}'


# 云端服务异常
class ServerException(SpiderException):
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg
        super().__init__()

    def __str__(self):
        return f'云端服务错误! code {self.code} msg {self.msg}'


# sdk本体错误信息
class SDKException(SpiderException):
    def __init__(self, msg: str):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return self.msg