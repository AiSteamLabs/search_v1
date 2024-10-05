from loguru import logger
from .base import SearchEngineBase
import os
import requests
from fastapi import HTTPException


# Search engine related. You don't really need to change this.
BING_SEARCH_V7_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
BING_MKT = "en-US"

class BingSearch(SearchEngineBase):
    def getInstanceFromEnv(self):
        self.search_api_key = os.environ["BING_SEARCH_V7_SUBSCRIPTION_KEY"]
        if self.search_api_key  and len(self.search_api_key)>0:
            return 
        else:
            raise RuntimeError("You shall specific api_key for BingSearch engine")
    
    def search(self, query, **kwargs):
        num_results = kwargs.get("num_results", 10)
        timeout = kwargs.get("timeout", 5)
        params = {"q": query, "mkt": BING_MKT}
        response = requests.get(
            BING_SEARCH_V7_ENDPOINT,
            headers={"Ocp-Apim-Subscription-Key": self.search_api_key },
            params=params,
            timeout=timeout,
        )
        if not response.ok:
            logger.error(f"{response.status_code} {response.text}")
            raise HTTPException(response.status_code, "Search engine error.")
        json_content = response.json()
        try:
            contexts = json_content["webPages"]["value"][:num_results]
        except KeyError:
            logger.error(f"Error encountered: {json_content}")
            return []
        return contexts