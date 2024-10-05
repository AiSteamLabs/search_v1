from .bing import BingSearch
from .exa_ai import EXAISearch
from .google_search import GoogleSearch
from .lepton import LeptonSearch

ModuleNamesMap = {
    "GOOGLE": GoogleSearch,
    "EXAI": EXAISearch,
    "LEPTON": LeptonSearch,
    "BING": BingSearch,   
}

