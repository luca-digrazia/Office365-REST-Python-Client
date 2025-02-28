from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.base_entity_collection import BaseEntityCollection
from office365.sharepoint.marketplace.app_metadata import CorporateCatalogAppMetadata


class SiteCollectionCorporateCatalogAccessor(BaseEntity):
    """Accessor for the site collection corporate catalog."""

    @property
    def available_apps(self):
        """Returns the apps available in this corporate catalog."""
        return self.properties.get('AvailableApps',
                                   BaseEntityCollection(self.context, CorporateCatalogAppMetadata,
                                                        ResourcePath("AvailableApps", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "AvailableApps": self.available_apps
            }
            default_value = property_mapping.get(name, None)
        return super(SiteCollectionCorporateCatalogAccessor, self).get_property(name, default_value)
