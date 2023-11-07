'''
Created on Aug 1, 2013

@organization: cert.org
'''
from certfuzz.errors import CERTFuzzError


class CampaignError(CERTFuzzError):
    pass


class CampaignScriptError(CampaignError):
    pass

class CmdlineTemplateError(CampaignError):
    pass
