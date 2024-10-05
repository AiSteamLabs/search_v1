from loguru import logger
from .base import SearchEngineBase
import os
import requests
from fastapi import HTTPException

GOOGLE_SEARCH_ENDPOINT = "https://customsearch.googleapis.com/customsearch/v1"


class GoogleSearch(SearchEngineBase):
    def getInstanceFromEnv(self):
        key = os.getenv("GOOGLE_SEARCH_API_KEY")
        cx  = os.getenv("GOOGLE_SEARCH_CX")
        if key and cx:
            self.params = {
                "key": key,
                "cx": cx,
            }
        else:
            raise RuntimeError("You shall specific api_key for GoogleSearch engine")
    
    def convert_google_to_bing(self, google_contexts):
        bing_contexts = []
        for id, item in enumerate(google_contexts):
            if item.get("snippet",None) == None: continue
            bing_item = {
                "id":  id, 
                "name": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet"),
                "displayUrl": item.get("displayLink"),
            }
            bing_contexts.append(bing_item)
        return bing_contexts
    
    def search(self, query, **kwargs):
        params = dict(self.params)
        params["q"] =  query
        params["num"] = kwargs.get("num_results", 10)
        response = requests.get(
                GOOGLE_SEARCH_ENDPOINT, params=params, timeout= kwargs.get("timeout", 5)
            )
        if not response.ok:
            logger.error(f"{response.status_code} {response.text}")
            raise HTTPException(response.status_code, "Search engine error.")
        json_content = response.json()
        try:
            contexts = json_content["items"]
            contexts = self.convert_google_to_bing(contexts)
        except KeyError:
            logger.error(f"Error encountered: {json_content}")
            return []
        return contexts




    
