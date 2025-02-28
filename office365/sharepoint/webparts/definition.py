from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.webparts.webpart import WebPart


class WebPartDefinition(BaseEntity):
    """Represents a Web Part on a Web Part Page. Provides operations for moving, deleting, and changing the state of
    the Web Part."""

    def web_part(self):
        """The WebPart object (1), as specified in section 3.2.5.148, associated with this WebPartDefinition.
        The WebPart object (1) contains additional properties relating to the Web Part represented by this
        WebPartDefinition object"""
        return self.properties.get('WebPart',
                                   WebPart(self.context, ResourcePath("WebPart", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "WebPart": self.web_part
            }
            default_value = property_mapping.get(name, None)
        return super(WebPartDefinition, self).get_property(name, default_value)
