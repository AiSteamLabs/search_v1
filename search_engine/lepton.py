from loguru import logger
from .base import SearchEngineBase
import os

import leptonai
from leptonai import Client
from leptonai.api.workspace import WorkspaceInfoLocalRecord
from leptonai.photon.types import to_bool
import httpx


class LeptonSearch(SearchEngineBase):
    def getInstanceFromEnv(self):
        leptonai.api.workspace.login()
        self.token = os.environ.get("LEPTON_WORKSPACE_TOKEN") or WorkspaceInfoLocalRecord.get_current_workspace_token()
        self.stream = to_bool(os.environ.get("STREAM_MODE"))
        self.timeout = httpx.Timeout(connect=10, read=120, write=120, pool=10)
        if self.token and len(self.token)>0:
            self.leptonsearch_client = Client(
                "https://search-api.lepton.run/",
                token=self.token,
                stream=self.stream,
                timeout=self.timeout
            )
        if self.leptonsearch_client: 
            return True
        else:
            raise RuntimeError("You shall specific api_key for LeptonSearch engine")
    
    def search(self, query, **kwargs):
        search_uuid = kwargs.get("search_uuid", None)
        stream      = kwargs.get("stream", False)
        generate_related_questions      = kwargs.get("generate_related_questions", False)
        return self.leptonsearch_client.query(
                query=query,
                stream=stream,
                search_uuid=search_uuid,
                generate_related_questions=generate_related_questions,
            )
    
            