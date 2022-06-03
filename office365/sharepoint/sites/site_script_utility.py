from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation_query import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.base_entity_collection import BaseEntityCollection
from office365.sharepoint.sitedesigns.site_design_metadata import SiteDesignMetadata
from office365.sharepoint.sitedesigns.site_script_metadata import SiteScriptMetadata
from office365.sharepoint.sitedesigns.site_design_principal import SiteDesignPrincipal
from office365.sharepoint.webs.site_scripts import SiteScriptSerializationResult, SiteScriptSerializationInfo


class SiteScriptUtility(BaseEntity):
    """Use class to automate provisioning new or existing modern
    SharePoint sites that use your own custom configurations.
    """

    def __init__(self, context):
        path = ResourcePath("Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUtility")
        super(SiteScriptUtility, self).__init__(context, path)

    @staticmethod
    def get_site_script_from_list(context, list_url, options=None, return_type=None):
        """
        Creates site script syntax from an existing SharePoint list.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        :param str list_url:  URL of the list.
        :param dict or None options:
        :param ClientResult return_type:  Return type
        """
        if return_type is None:
            return_type = ClientResult(context)
        payload = {
            "listUrl": list_url,
            "options": options
        }
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteScriptFromList", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_script_from_web(context, web_url, info=None, return_type=None):
        """
        Creates site script syntax from an existing SharePoint site.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        :param str web_url:  URL of the web.
        :param SiteScriptSerializationInfo or None info:
        :param ClientResult return_type:  Return type
        """
        if return_type is None:
            return_type = ClientResult(context, SiteScriptSerializationResult())
        payload = {
            "webUrl": web_url,
            "info": info
        }
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteScriptFromWeb", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def create_site_script(context, title, description, content):
        """
        Creates a new site script.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        :param str title:
        :param str description:
        :param str content:
        """
        return_type = ClientResult(context, SiteScriptMetadata())
        utility = SiteScriptUtility(context)
        payload = {
            "Title": title,
            "Description": description,
            "Content": content
        }
        qry = ServiceOperationQuery(utility, "CreateSiteScript", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_scripts(context, store=None):
        """
        Gets a list of information on all existing site scripts.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        :param str store:
        """
        return_type = ClientResult(context, ClientValueCollection(SiteScriptMetadata))
        utility = SiteScriptUtility(context)
        payload = {
            "store": store
        }
        qry = ServiceOperationQuery(utility, "GetSiteScripts", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_design_metadata(context, _id, store=None):
        """
        Gets information about a specific site script.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint context
        :param str _id:
        :param str store:
        """
        return_type = ClientResult(context, SiteDesignMetadata())
        utility = SiteScriptUtility(context)
        payload = {
            "id": _id,
            "store": store
        }
        qry = ServiceOperationQuery(utility, "GetSiteDesignMetadata", None, payload, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def get_site_design_rights(context, _id):
        """
        Gets a list of principals that have access to a site design.

        :type _id: str
        :param office365.sharepoint.client_context.ClientContext context: SharePoint client

        """
        return_type = BaseEntityCollection(context, SiteDesignPrincipal)
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "GetSiteDesignRights", [_id], None, None, return_type)
        qry.static = True
        context.add_query(qry)
        return return_type

    @staticmethod
    def grant_site_design_rights(context, _id, principal_names, granted_rights):
        """Grants access to a site design for one or more principals.

        :param office365.sharepoint.client_context.ClientContext context: SharePoint client
        :param str _id:
        :param list[str] principal_names:
        :param long granted_rights:
        """
        utility = SiteScriptUtility(context)
        payload = {
            "id": _id,
            "principalNames": ClientValueCollection(str, principal_names),
            "grantedRights": granted_rights
        }
        qry = ServiceOperationQuery(utility, "GrantSiteDesignRights", None, payload)
        qry.static = True
        context.add_query(qry)
        return utility

    @staticmethod
    def delete_site_design(context, _id):
        """
        Deletes a site design.

        :type _id: str
        :param office365.sharepoint.client_context.ClientContext context: SharePoint client
        """
        utility = SiteScriptUtility(context)
        qry = ServiceOperationQuery(utility, "DeleteSiteDesign", [_id])
        qry.static = True
        context.add_query(qry)
        return utility

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptUtility"
