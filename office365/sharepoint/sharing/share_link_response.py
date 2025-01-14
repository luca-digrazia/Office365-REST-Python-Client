from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharing.sharing_link_info import SharingLinkInfo


class ShareLinkResponse(ClientValue):
    """
    Represents a response for a request for the retrieval or creation/update of a tokenized sharing link.
    """
    def __init__(self, sharing_link_info=SharingLinkInfo()):
        self.sharingLinkInfo = sharing_link_info
