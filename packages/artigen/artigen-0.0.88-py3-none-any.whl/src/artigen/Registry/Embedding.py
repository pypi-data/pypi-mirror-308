from .BaseRegistry import BaseRegistry


class Embedding(BaseRegistry):
    def __init__(self, api_key):
        self.api_key = api_key

    async def create_darn(self, **kwargs):
        pass

    async def update_darn(self, **kwargs):
        pass

    async def list_darn(self, **kwargs):
        pass

    async def delete_darn(self, **kwargs):
        pass
