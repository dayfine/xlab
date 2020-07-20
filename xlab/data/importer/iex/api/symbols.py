from xlab.data.importer.iex.api import base


class IexSymbolsApi:

    def __init__(self, token: str = ''):
        self._client = base.SimpleIexApiHttpClient(token, 'ref-data/symbols',
                                                   lambda: {})

    def get_symbols(self):
        return self._client.call()
