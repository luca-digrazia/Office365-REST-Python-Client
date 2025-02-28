from office365.runtime.client_result import ClientResult
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.publishing.sites.communication.creation_request import CommunicationSiteCreationRequest
from office365.sharepoint.publishing.sites.communication.creation_response import CommunicationSiteCreationResponse


class CommunicationSite(BaseEntity):
    """Represents a Communication Site."""

    def create(self, alias, title):
        """
        Initiates creation of a Communication Site.

        - If the SiteStatus returns 1, the Communication Site is in the process of being created asynchronously.

        - If the SiteStatus returns 2 and the SiteUrl returns a non-empty, non-null value, the site was created
        synchronously and is available at the specified URL.

        - If the SiteStatus returns 2 and the SiteUrl returns an empty or null value, the site already exists but is
        inaccessible for some reason, such as being "locked".

        - If the SiteStatus returns 3 or 0, the Communication site failed to be created.

        :param str alias: Site alias which defines site url, e.g. https://contoso.sharepoint.com/sites/{alias}
        :param str title: Site title
        """
        site_url = "{base_url}/sites/{alias}".format(base_url=self.context.base_url, alias=alias)
        request = CommunicationSiteCreationRequest(title, site_url)
        result = ClientResult(self.context, CommunicationSiteCreationResponse())
        qry = ServiceOperationQuery(self, "Create", None, request, "request", result)
        self.context.add_query(qry)
        return result

    def get_status(self, site_url):
        """
        Retrieves the status of creation of a Communication site.

        If the SiteStatus returned is 0, then no work item for a site with the specified URL was found, and no site was
        found with the specified URL. This could mean either that a creation attempt hasn’t started yet, or that it
        failed with a “non-retryable” exception and did not preserve a work item for further attempts.

        If the SiteStatus returns 1, the Communication Site is in the process of being created asynchronously.

        If the SiteStatus returns 2 and the SiteUrl returns a non-empty, non-null value, the site was created
        synchronously and is available at the specified URL.

        If the SiteStatus returns 2 and the SiteUrl returns an empty or null value, the site already exists but
        is inaccessible for some reason, such as being “locked”.

        If the SiteStatus returns 3 or 0, the Communication site failed to be created.
        """
        response = ClientResult(self.context, CommunicationSiteCreationResponse())
        qry = ServiceOperationQuery(self, "Status", None, {'url': site_url}, None, response)
        self.context.add_query(qry)

        def _construct_status_request(request):
            request.method = HttpMethod.Get
            request.url += "?url='{0}'".format(site_url)

        self.context.before_execute(_construct_status_request)
        return response

    def enable(self, design_package_id):
        qry = ServiceOperationQuery(self, "Enable", None, {"designPackageId": design_package_id})
        self.context.add_query(qry)
        return self

    @property
    def entity_type_name(self):
        return "SP.Publishing.CommunicationSite"
