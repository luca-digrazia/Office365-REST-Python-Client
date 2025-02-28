import uuid

from tests.graph_case import GraphTestCase

from office365.teams.channels.channel import Channel
from office365.teams.chats.message import ChatMessage
from office365.outlook.mail.itemBody import ItemBody
from office365.teams.team import Team


class TestGraphChannel(GraphTestCase):
    """Tests for channels"""

    target_team = None  # type: Team
    target_channel = None  # type: Channel
    target_message = None  # type: ChatMessage

    @classmethod
    def setUpClass(cls):
        super(TestGraphChannel, cls).setUpClass()
        team_name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create(team_name).execute_query()
        cls.target_team = team

    @classmethod
    def tearDownClass(cls):
        cls.target_team.delete_object().execute_query_retry()

    def test1_get_team(self):
        team = self.__class__.target_team.get().execute_query()
        self.assertIsNotNone(team.id)

    def test2_get_channels(self):
        channels = self.__class__.target_team.channels.get().execute_query()
        self.assertGreater(len(channels), 0)

    def test3_create_channel(self):
        channel_name = "Channel_" + uuid.uuid4().hex
        new_channel = self.__class__.target_team.channels.add(channel_name).execute_query()
        self.assertIsNotNone(new_channel.resource_path)
        self.__class__.target_channel = new_channel

    def test4_get_channel(self):
        channel_id = self.__class__.target_channel.id
        existing_channel = self.__class__.target_team.channels[channel_id].get().execute_query()
        self.assertEqual(existing_channel.id, channel_id)

    def test5_get_primary_channel(self):
        primary_channel = self.__class__.target_team.primary_channel.get().execute_query()
        self.assertIsNotNone(primary_channel.resource_path)

    # def test6_get_channel_files_location(self):
    #    drive_item = self.__class__.target_channel.filesFolder.get().execute_query()
    #    self.assertIsNotNone(drive_item.resource_path)

    def test7_send_message(self):
        item_body = ItemBody("Hello world!")
        message = self.__class__.target_channel.messages.add(body=item_body).execute_query()
        self.assertIsNotNone(message.id)
        self.__class__.target_message = message

    def test8_reply_to_message(self):
        item_body = ItemBody("Hello world back!")
        reply = self.__class__.target_message.replies.add(body=item_body).execute_query()
        self.assertIsNotNone(reply.id)

    def test9_delete_channel(self):
        channels_before = self.__class__.target_team.channels.get().execute_query()
        self.__class__.target_channel.delete_object().execute_query()
        channels_after = self.__class__.target_team.channels.get().execute_query()
        self.assertEqual(len(channels_before)-1, len(channels_after))
