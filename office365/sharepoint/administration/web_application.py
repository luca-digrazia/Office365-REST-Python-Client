from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.base_entity_collection import BaseEntityCollection
from office365.sharepoint.sites.site import Site


class WebApplication(BaseEntity):

    @staticmethod
    def lookup(context, request_uri):
        """
        :type context
        :type request_uri str
        """
        return_type = WebApplication(context)
        payload = {"requestUri": request_uri}
        qry = ServiceOperationQuery(return_type, "Lookup", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @property
    def outbound_mail_sender_address(self):
        """
        :rtype: str or None
        """
        return self.properties.get("OutboundMailSenderAddress", None)

    @property
    def sites(self):
        return self.properties.get('Sites',
                                   BaseEntityCollection(self.context, Site, ResourcePath("Sites", self.resource_path)))

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.SPWebApplication"
