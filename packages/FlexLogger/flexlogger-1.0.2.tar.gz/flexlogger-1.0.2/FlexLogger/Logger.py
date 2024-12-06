import socket

import requests

from FlexLogger.Log import Classification


class Logger:
    application: str

    def __init__(self, endpoint_server: str, endpoint_port: int, endpoint_command: str, api_token: str, application: str):
        self.application = application

        # API and Token prepare
        self.__api_url = f"https://{endpoint_server}:{endpoint_port}/{endpoint_command}"
        self.__token = api_token

        if socket.gethostname() == endpoint_server:
            self.__source = "Local"
        else:
            self.__source = "Remote"

    def smartSend(self, title: str, classification: Classification, contents: str = None):
        body = {
          "application": self.application,
          "source": self.__source,
          "title": f"{title}",
          "category": classification.value[0],
          "category2": classification.value[1],
          "contents": f"{contents}",
          "SYSLOG_LEVELS_code": classification.value[2].value
        }

        self.__send(body)

    def fullSend(self, title: str, source: str, category: str, category2: str, syslogLevel: int, contents: str):
        body = {
            "application": self.application,
            "source": f"{source}",
            "title": f"{title}",
            "category": f"{category}",
            "category2": f"{category2}",
            "contents": f"{contents}",
            "SYSLOG_LEVELS_code": syslogLevel
        }

        self.__send(body)

    def __send(self, body: dict):

        # Fazendo a chamada POST
        requests.post(url=self.__api_url,
                      headers={ "Authorization": f"Bearer {self.__token}", "Content-Type": "application/json" },
                      json=body)