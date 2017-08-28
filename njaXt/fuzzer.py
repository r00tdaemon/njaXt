from PyQt5.QtWebEngineCore import QWebEngineHttpRequest
from PyQt5.QtCore import QUrl


class Request:
    def __init__(self, req: dict):
        self._request = req
        self._headers = self._request.get("headers", "").splitlines()

    @property
    def url(self):
        return self._request.get("url", "")

    @property
    def method(self):
        return self._request.get("method", "GET")

    @property
    def headers(self):
        return [header.split(":") for header in self._headers]

    @property
    def post_data(self):
        return self._request.get("post_data", "")


class Fuzzer:
    def __init__(self, req: dict):
        self.request = Request(req)

    def requests(self, payloads: str):
        for payload in payloads.splitlines():
            url = self.request.url.replace("[X]", payload)
            url = QUrl.fromUserInput(url)
            req = QWebEngineHttpRequest(url)
            req.setMethod(
                QWebEngineHttpRequest.Get if self.request.method == "GET"
                else QWebEngineHttpRequest.Post
            )
            for header in self.request.headers:
                req.setHeader(header[0].encode(), header[1].encode())

            if self.request.method == "POST" and self.request.post_data:
                req.setPostData(self.request.post_data.encode())

            yield req
