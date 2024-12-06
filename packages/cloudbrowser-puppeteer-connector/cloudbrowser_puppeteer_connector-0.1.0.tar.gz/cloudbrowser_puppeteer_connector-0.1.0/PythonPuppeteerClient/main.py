import aiohttp
import asyncio
from pyppeteer import connect

class CloudBrowserConnector:
    def __init__(self, api_token, body=None):
        self.api_token = api_token
        self.server_url = 'https://production.cloudbrowser.ai/api/v1/Browser/OpenAdvanced'
        self.body = body

    async def get_websocket_url(self):
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.server_url, json=self.body, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch WebSocket URL: {response.reason}")
                
                json_response = await response.json()
                return json_response['address']

    async def connect(self):
        try:
            websocket_url = await self.get_websocket_url()
            browser = await connect(browserWSEndpoint=websocket_url)
            print('Connected to remote browser')
            return browser
        except Exception as e:
            print(f'Error connecting to remote browser: {str(e)}')
            raise

