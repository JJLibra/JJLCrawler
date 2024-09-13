from httpx import RequestError


class DataFetchError(RequestError):
    pass


class IPBlockError(RequestError):
    pass
