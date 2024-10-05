from exa_py import Exa
from .base import SearchEngineBase
import os

class EXAISearch(SearchEngineBase):
    def getInstanceFromEnv(self):
        self.api_key = os.getenv("EXAI_API_KEY")
        if self.api_key and len(self.api_key)>0:
            self.exa = Exa(api_key=self.api_key)
        else:
            raise RuntimeError("You shall specific api_key for EXAISearch engine")
    
    def search(self, query, **kwargs):
        num_results = kwargs.get("num_results", 8)
        resp = self.exa.search_and_contents(
                    query,
                    type="neural",
                    use_autoprompt=True,
                    num_results=num_results,
                    text=True
                    )
        
        search_ret = []
        for item in resp.results:
            bing_item = {
                "id":  item.id, 
                "name": item.title,
                "url": item.url,
                "snippet": item.text.replace(" \n\n",""),
                "displayUrl": item.url,
            }
            item.text = item.text.replace(" \n\n","")
            if len(item.text)>350:
                bing_item["snippet"] = item.text[:350]
            else:
                bing_item["snippet"] = item.text
            search_ret.append(bing_item)
        return search_ret
