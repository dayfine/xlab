import os
from xlab.data.provider import DataProvider


class IexDataProvider(DataProvider):
    def __init__(self):
        self.session = requests.Session()
        self.token = os.getenv('IEX_API_SECRET_TOKEN')

    def get_quote():
        pass
