from office365.communications.onlinemeetings.collection import OnlineMeetingCollection
from office365.communications.presences.presence import Presence
from office365.delta_collection import DeltaCollection
from office365.directory.extensions.extension import Extension
from office365.directory.licenses.assigned_plan import AssignedPlan
from office365.directory.users.settings import UserSettings
from office365.onedrive.sites.site import Site
from office365.onenote.onenote import Onenote
from office365.outlook.calendar.attendee_base import AttendeeBase
from office365.outlook.calendar.calendar import Calendar
from office365.outlook.calendar.group import CalendarGroup
from office365.outlook.calendar.event import Event
from office365.outlook.calendar.meeting_time_suggestions_result import MeetingTimeSuggestionsResult
from office365.outlook.calendar.reminder import Reminder
from office365.directory.licenses.assigned_license import AssignedLicense
from office365.directory.directory_object import DirectoryObject
from office365.directory.directory_object_collection import DirectoryObjectCollection
from office365.directory.licenses.license_details import LicenseDetails
from office365.directory.identities.object_identity import ObjectIdentity
from office365.directory.profile_photo import ProfilePhoto
from office365.entity_collection import EntityCollection
from office365.outlook.contacts.contact import Contact
from office365.outlook.contacts.folder import ContactFolder
from office365.outlook.mail.folder import MailFolder
from office365.onedrive.drives.drive import Drive
from office365.outlook.mail.mailbox_settings import MailboxSettings
from office365.outlook.mail.messages.collection import MessageCollection
from office365.outlook.mail.messages.message import Message
from office365.outlook.mail.recipient import Recipient
from office365.outlook.user import OutlookUser
from office365.planner.user import PlannerUser
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.http.http_method import HttpMethod
from office365.runtime.paths.entity import EntityPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.collections import StringCollection
from office365.teams.chats.collection import ChatCollection
from office365.teams.collection import TeamCollection
from office365.teams.user_teamwork import UserTeamwork
from office365.todo.todo import Todo


class User(DirectoryObject):
    """Represents an Azure AD user account. Inherits from directoryObject."""

    def assign_license(self, add_licenses, remove_licenses):
        """
        Add or remove licenses on the user.

        :param list[str] remove_licenses: A collection of skuIds that identify the licenses to remove.
        :param list[AssignedLicense] add_licenses: A collection of assignedLicense objects that specify
             the licenses to add.
        """
        params = {
            "addLicenses": ClientValueCollection(AssignedLicense, add_licenses),
            "removeLicenses": StringCollection(remove_licenses)
        }
        qry = ServiceOperationQuery(self, "assignLicense", None, params, None, self)
        self.context.add_query(qry)
        return self

    def change_password(self, current_password, new_password):
        """

        :param str current_password:
        :param str new_password:
        """
        qry = ServiceOperationQuery(self, "changePassword", None,
                                    {"currentPassword": current_password, "newPassword": new_password})
        self.context.add_query(qry)
        return self

    def send_mail(self, subject, body, to_recipients, save_to_sent_items=False):
        """Send a new message on the fly

        :param str subject: The subject of the message.
        :param str body: The body of the message. It can be in HTML or text format
        :param list[str] to_recipients: The To: recipients for the message.
        :param bool save_to_sent_items: Indicates whether to save the message in Sent Items. Specify it only if
            the parameter is false; default is true
        """
        message = Message(self.context)
        message.subject = subject
        message.body = body
        [message.to_recipients.add(Recipient.from_email(email)) for email in to_recipients]

        payload = {
            "message": message,
            "saveToSentItems": save_to_sent_items
        }
        qry = ServiceOperationQuery(self, "sendmail", None, payload)
        self.context.add_query(qry)
        return message

    def export_personal_data(self, storage_location):
        """
        Submit a data policy operation request from a company administrator or an application to
        export an organizational user's data.

        If successful, this method returns a 202 Accepted response code.
        It does not return anything in the response body. The response contains the following response headers.

        :param str storage_location: This is a shared access signature (SAS) URL to an Azure Storage account,
            to where data should be exported.
        """
        qry = ServiceOperationQuery(self, "exportPersonalData", None, {"storage_location": storage_location})
        self.context.add_query(qry)
        return self

    def find_meeting_times(self, attendees=None, location_constraint=None):
        """
        Suggest meeting times and locations based on organizer and attendee availability, and time or location
        constraints specified as parameters.

        If findMeetingTimes cannot return any meeting suggestions, the response would indicate a reason in the
        emptySuggestionsReason property. Based on this value, you can better adjust the parameters
        and call findMeetingTimes again.

        The algorithm used to suggest meeting times and locations undergoes fine-tuning from time to time.
        In scenarios like test environments where the input parameters and calendar data remain static, expect
        that the suggested results may differ over time.

        :param list[AttendeeBase] or None attendees: A collection of attendees or resources for the meeting.
            Since findMeetingTimes assumes that any attendee who is a person is always required, specify required
            for a person and resource for a resource in the corresponding type property. An empty collection causes
            findMeetingTimes to look for free time slots for only the organizer. Optional.
        :param office365.outlook.calendar.location_constraint.LocationConstraint or None location_constraint:
            The organizer's requirements about the meeting location, such as whether a suggestion for a meeting
            location is required, or there are specific locations only where the meeting can take place. Optional.
        """
        payload = {
            "attendees": ClientValueCollection(AttendeeBase, attendees),
            "locationConstraint": location_constraint
        }
        result = ClientResult(self.context, MeetingTimeSuggestionsResult())
        qry = ServiceOperationQuery(self, "findMeetingTimes", None, payload, None, result)
        self.context.add_query(qry)
        return result

    def get_calendar_view(self, start_dt, end_dt):
        """Get the occurrences, exceptions, and single instances of events in a calendar view defined by a time range,
           from the user's default calendar, or from some other calendar of the user's.

        :param datetime.datetime end_dt: The end date and time of the time range, represented in ISO 8601 format.
             For example, "2019-11-08T20:00:00-08:00".
        :param datetime.datetime start_dt: The start date and time of the time range, represented in ISO 8601 format.
            For example, "2019-11-08T19:00:00-08:00".

        """
        return_type = EntityCollection(self.context, Event, ResourcePath("calendarView", self.resource_path))
        qry = ServiceOperationQuery(self, "calendarView", None, None, None, return_type)
        self.context.add_query(qry)

        def _construct_request(request):
            """
            :type request: office365.runtime.http.request_options.RequestOptions
            """
            request.method = HttpMethod.Get
            request.url += "?startDateTime={0}&endDateTime={1}".format(start_dt.isoformat(), end_dt.isoformat())

        self.context.before_execute(_construct_request)
        return return_type

    def get_reminder_view(self, start_dt, end_dt):
        """Get the occurrences, exceptions, and single instances of events in a calendar view defined by a time range,
                   from the user's default calendar, or from some other calendar of the user's.

        :param datetime.datetime end_dt: The end date and time of the event for which the reminder is set up.
            The value is represented in ISO 8601 format, for example, "2015-11-08T20:00:00.0000000"..
        :param datetime.datetime start_dt: The start date and time of the event for which the reminder is set up.
            The value is represented in ISO 8601 format, for example, "2015-11-08T19:00:00.0000000".
        """
        result = ClientResult(self.context, ClientValueCollection(Reminder))
        params = {
            "startDateTime": start_dt.isoformat(),
            "endDateTime": end_dt.isoformat(),
        }
        qry = ServiceOperationQuery(self, "reminderView", params, None, None, result)
        self.context.add_query(qry)

        def _construct_request(request):
            request.method = HttpMethod.Get

        self.context.before_execute(_construct_request)
        return result

    def delete_object(self, permanent_delete=False):
        """
        :param permanent_delete: Permanently deletes the user from directory
        :type permanent_delete: bool

        """
        super(User, self).delete_object()
        if permanent_delete:
            deleted_user = self.context.directory.deleted_users[self.id]
            deleted_user.delete_object()
        return self

    def revoke_signin_sessions(self):
        """
        Invalidates all the refresh tokens issued to applications for a user
        (as well as session cookies in a user's browser), by resetting the signInSessionsValidFromDateTime user
        property to the current date-time. Typically, this operation is performed (by the user or an administrator)
        if the user has a lost or stolen device. This operation prevents access to the organization's data through
        applications on the device by requiring the user to sign in again to all applications that they have previously
        consented to, independent of device.
        """
        result = ClientResult(self.context)
        qry = ServiceOperationQuery(self, "revokeSignInSessions", None, None, None, result)
        self.context.add_query(qry)
        return result

    def reprocess_license_assignment(self):
        """
        Reprocess all group-based license assignments for the user. To learn more about group-based licensing,
        see What is group-based licensing in Azure Active Directory. Also see Identify and resolve license assignment
        problems for a group in Azure Active Directory for more details.
        """
        return_type = User(self.context)
        qry = ServiceOperationQuery(self, "reprocessLicenseAssignment", None, None, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def account_enabled(self):
        """True if the account is enabled; otherwise, false. This property is required when a user is created."""
        return self.properties.get('accountEnabled', None)

    @property
    def chats(self):
        """The user's chats."""
        return self.properties.get('chats',
                                   ChatCollection(self.context, ResourcePath("chats", self.resource_path)))

    @property
    def given_name(self):
        """
        The given name (first name) of the user. Maximum length is 64 characters.

        :rtype: str or None
        """
        return self.properties.get('givenName', None)

    @property
    def user_principal_name(self):
        """
        The user principal name (UPN) of the user. The UPN is an Internet-style login name for the user based on the
        Internet standard RFC 822. By convention, this should map to the user's email name.
        The general format is alias@domain, where domain must be present in the tenant's collection of verified domains.
        This property is required when a user is created. The verified domains for the tenant can be accessed from
        the verifiedDomains property of organization.
        NOTE: This property cannot contain accent characters.
        Only the following characters are allowed A - Z, a - z, 0 - 9, ' . - _ ! # ^ ~.
        For the complete list of allowed characters, see username policies.

        :rtype: str or None
        """
        return self.properties.get('userPrincipalName', None)

    @property
    def assigned_plans(self):
        """The plans that are assigned to the user."""
        return self.properties.get('assignedPlans', ClientValueCollection(AssignedPlan))

    @property
    def business_phones(self):
        """String collection	The telephone numbers for the user. NOTE: Although this is a string collection,
        only one number can be set for this property. Read-only for users synced from on-premises directory.
        """
        return self.properties.get('businessPhones', StringCollection())

    @property
    def creation_type(self):
        """Indicates whether the user account was created as a regular school or work account (null),
        an external account (Invitation), a local account for an Azure Active Directory B2C tenant (LocalAccount)
        or self-service sign-up using email verification (EmailVerified). Read-only.
        """
        return self.properties.get('creationType', None)

    @property
    def mail(self):
        """The SMTP address for the user, for example, "jeff@contoso.onmicrosoft.com".
           Returned by default. Supports $filter and endsWith.
        """
        return self.properties.get('mail', None)

    @property
    def other_mails(self):
        """A list of additional email addresses for the user;
        for example: ["bob@contoso.com", "Robert@fabrikam.com"]. Supports $filter.
        """
        return self.properties.get('otherMails', StringCollection())

    @property
    def identities(self):
        """Represents the identities that can be used to sign in to this user account.
           An identity can be provided by Microsoft (also known as a local account), by organizations,
           or by social identity providers such as Facebook, Google, and Microsoft, and tied to a user account.
           May contain multiple items with the same signInType value.
           Supports $filter.
        """
        return self.properties.get('identities', ClientValueCollection(ObjectIdentity))

    @property
    def assigned_licenses(self):
        """The licenses that are assigned to the user, including inherited (group-based) licenses. """
        return self.properties.get('assignedLicenses', ClientValueCollection(AssignedLicense))

    @property
    def followed_sites(self):
        """

        """
        return self.properties.get('followedSites',
                                   EntityCollection(self.context, Site,
                                                    ResourcePath("followedSites", self.resource_path)))

    @property
    def photo(self):
        """
        The user's profile photo. Read-only.
        """
        return self.properties.get('photo',
                                   ProfilePhoto(self.context, ResourcePath("photo", self.resource_path)))

    @property
    def manager(self):
        """
        The user or contact that is this user's manager. Read-only. (HTTP Methods: GET, PUT, DELETE.)
        """
        return self.properties.get('manager',
                                   DirectoryObject(self.context, ResourcePath("manager", self.resource_path)))

    @property
    def preferred_language(self):
        """
        The preferred language for the user. Should follow ISO 639-1 Code; for example en-US.

        :rtype: str or None
        """
        return self.properties.get('preferredLanguage', None)

    @property
    def mailbox_settings(self):
        """
        Get the user's mailboxSettings.

        :rtype: str or None
        """
        return self.properties.get('mailboxSettings', MailboxSettings())

    @property
    def calendar(self):
        """The user's primary calendar. Read-only."""
        return self.properties.get('calendar',
                                   Calendar(self.context, ResourcePath("calendar", self.resource_path)))

    @property
    def calendars(self):
        """The user's calendar groups. Read-only. Nullable."""
        return self.properties.get('calendars',
                                   EntityCollection(self.context, Calendar,
                                                    ResourcePath("calendars", self.resource_path)))

    @property
    def calendar_groups(self):
        """The user's calendar groups. Read-only. Nullable."""
        return self.properties.get('calendarGroups',
                                   EntityCollection(self.context, CalendarGroup,
                                                    ResourcePath("calendarGroups", self.resource_path)))

    @property
    def license_details(self):
        """Retrieve the properties and relationships of a Drive resource."""
        return self.properties.get('licenseDetails',
                                   EntityCollection(self.context, LicenseDetails,
                                                    ResourcePath("licenseDetails", self.resource_path)))

    @property
    def drive(self):
        """Retrieve the properties and relationships of a Drive resource."""
        return self.properties.get('drive',
                                   Drive(self.context, EntityPath("drive", self.resource_path, ResourcePath("drives"))))

    @property
    def contacts(self):
        """Get a contact collection from the default Contacts folder of the signed-in user (.../me/contacts),
        or from the specified contact folder."""
        return self.properties.get('contacts',
                                   DeltaCollection(self.context, Contact,
                                                   ResourcePath("contacts", self.resource_path)))

    @property
    def contact_folders(self):
        """Get the contact folder collection in the default Contacts folder of the signed-in user."""
        return self.properties.get('contactFolders',
                                   DeltaCollection(self.context, ContactFolder,
                                                   ResourcePath("contactFolders", self.resource_path)))

    @property
    def events(self):
        """Get an event collection or an event."""
        return self.properties.get('events', DeltaCollection(self.context, Event,
                                                             ResourcePath("events", self.resource_path)))

    @property
    def messages(self):
        """Get an event collection or an event."""
        return self.properties.get('messages',
                                   MessageCollection(self.context, ResourcePath("messages", self.resource_path)))

    @property
    def joined_teams(self):
        """Get the teams in Microsoft Teams that the user is a direct member of."""
        return self.properties.get('joinedTeams',
                                   TeamCollection(self.context, ResourcePath("joinedTeams", self.resource_path)))

    @property
    def member_of(self):
        """Get groups and directory roles that the user is a direct member of."""
        return self.properties.get('memberOf',
                                   DirectoryObjectCollection(self.context,
                                                             ResourcePath("memberOf", self.resource_path)))

    @property
    def transitive_member_of(self):
        """Get groups, directory roles that the user is a member of. This API request is transitive, and will also
        return all groups the user is a nested member of. """
        return self.properties.get('transitiveMemberOf',
                                   DirectoryObjectCollection(self.context,
                                                             ResourcePath("transitiveMemberOf", self.resource_path)))

    @property
    def mail_folders(self):
        """Get the mail folder collection under the root folder of the signed-in user. """
        return self.properties.get('mailFolders',
                                   DeltaCollection(self.context, MailFolder,
                                                   ResourcePath("mailFolders", self.resource_path)))

    @property
    def outlook(self):
        """Represents the Outlook services available to a user."""
        return self.properties.get('outlook',
                                   OutlookUser(self.context, ResourcePath("outlook", self.resource_path)))

    @property
    def onenote(self):
        """Represents the Onenote services available to a user."""
        return self.properties.get('onenote',
                                   Onenote(self.context, ResourcePath("onenote", self.resource_path)))

    @property
    def settings(self):
        """Represents the user and organization settings object."""
        return self.properties.get('settings',
                                   UserSettings(self.context, ResourcePath("settings", self.resource_path)))

    @property
    def planner(self):
        """The plannerUser resource provide access to Planner resources for a user."""
        return self.properties.get('planner',
                                   PlannerUser(self.context, ResourcePath("planner", self.resource_path)))

    @property
    def extensions(self):
        """The collection of open extensions defined for the user. Nullable.

        :rtype: EntityCollection
        """
        return self.properties.get('extensions',
                                   EntityCollection(self.context, Extension,
                                                    ResourcePath("extensions", self.resource_path)))

    @property
    def direct_reports(self):
        """
        Get a user's direct reports.

        :rtype: EntityCollection
        """
        return self.properties.get('directReports',
                                   DirectoryObjectCollection(self.context,
                                                             ResourcePath("directReports", self.resource_path)))

    @property
    def online_meetings(self):
        """
        Get a user's online meetings.

        :rtype: OnlineMeetingCollection
        """
        return self.properties.get('onlineMeetings',
                                   OnlineMeetingCollection(self.context,
                                                           ResourcePath("onlineMeetings", self.resource_path)))

    @property
    def presence(self):
        """Get a user's presence information."""
        return self.properties.get('presence',
                                   Presence(self.context, ResourcePath("presence", self.resource_path)))

    @property
    def teamwork(self):
        """A container for the range of Microsoft Teams functionalities that are available per user in the tenant."""
        return self.properties.get('teamwork',
                                   UserTeamwork(self.context, ResourcePath("teamwork", self.resource_path)))

    @property
    def todo(self):
        """Represents the To Do services available to a user."""
        return self.properties.get('todo',
                                   Todo(self.context, ResourcePath("todo", self.resource_path)))

    def get_property(self, name, default_value=None):
        if default_value is None:
            property_mapping = {
                "businessPhones": self.business_phones,
                "calendarGroups": self.calendar_groups,
                "contactFolders": self.contact_folders,
                "followedSites": self.followed_sites,
                "licenseDetails": self.license_details,
                "memberOf": self.member_of,
                "transitiveMemberOf": self.transitive_member_of,
                "joinedTeams": self.joined_teams,
                "assignedLicenses": self.assigned_licenses,
                "mailFolders": self.mail_folders,
                "mailboxSettings": self.mailbox_settings,
                "directReports": self.direct_reports
            }
            default_value = property_mapping.get(name, None)
        return super(User, self).get_property(name, default_value)

    def set_property(self, name, value, persist_changes=True):
        super(User, self).set_property(name, value, persist_changes)
        # fallback: create a new resource path
        if self._resource_path is None:
            if name == "id" or name == "userPrincipalName":
                self._resource_path = ResourcePath(value, self.parent_collection.resource_path)
        return self
