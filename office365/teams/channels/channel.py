from office365.entity_collection import EntityCollection
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value import ClientValue
from office365.runtime.compat import quote

from office365.entity import Entity
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.teams.members.conversation import ConversationMember
from office365.teams.chats.message import ChatMessage
from office365.teams.tabs.tab import TeamsTab


class ProvisionChannelEmailResult(ClientValue):
    pass


class Channel(Entity):
    """Teams are made up of channels, which are the conversations you have with your teammates"""

    def provision_email(self):
        """
        Provision an email address for a channel.

        Microsoft Teams doesn't automatically provision an email address for a channel by default.
        To have Teams provision an email address, you can call provisionEmail, or through the Teams user interface,
        select Get email address, which triggers Teams to generate an email address if it has not already provisioned
        one.

        To remove the email address of a channel, use the removeEmail method.
        """
        return_type = ClientResult(self.context, ProvisionChannelEmailResult())
        qry = ServiceOperationQuery(self, "provisionEmail", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_email(self):
        """
        Remove the email address of a channel.

        You can remove an email address only if it was provisioned using the provisionEmail method or through
        the Microsoft Teams client.
        """
        qry = ServiceOperationQuery(self, "removeEmail")
        self.context.add_query(qry)
        return self

    @property
    def files_folder(self):
        """Get the metadata for the location where the files of a channel are stored."""
        return self.properties.get('filesFolder',
                                   DriveItem(self.context, ResourcePath("filesFolder", self.resource_path)))

    @property
    def tabs(self):
        """A collection of all the tabs in the channel. A navigation property."""
        return self.properties.get('tabs',
                                   EntityCollection(self.context, TeamsTab, ResourcePath("tabs", self.resource_path)))

    @property
    def messages(self):
        """
        A collection of all the messages in the channel. A navigation property. Nullable.
        """
        return self.properties.get('messages',
                                   EntityCollection(self.context, ChatMessage,
                                                    ResourcePath("messages", self.resource_path)))

    @property
    def members(self):
        """A collection of membership records associated with the channel.

        :rtype: EntityCollection
        """
        return self.get_property('members',
                                 EntityCollection(self.context, ConversationMember,
                                                  ResourcePath("members", self.resource_path)))

    @property
    def web_url(self):
        """A hyperlink that will navigate to the channel in Microsoft Teams. This is the URL that you get when you
        right-click a channel in Microsoft Teams and select Get link to channel. This URL should be treated as an
        opaque blob, and not parsed. Read-only.

        :rtype: str or None """
        return self.properties.get('webUrl', None)

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "filesFolder": self.files_folder,
            }
            default_value = property_mapping.get(name, None)
        return super(Channel, self).get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super(Channel, self).set_property(name, value, persist_changes)
        # fallback: fix resource path
        if name == "id":
            channel_id = quote(value)
            self._resource_path = ResourcePath(channel_id, self.resource_path.parent)
        return self
