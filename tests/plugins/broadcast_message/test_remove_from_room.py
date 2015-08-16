import asynctest
from asynctest.mock import MagicMock
from asynctest.mock import CoroutineMock
from charlesbot.plugins.broadcast_message import BroadcastMessage
from charlesbot.slack.slack_group_left import SlackGroupLeft
from charlesbot.slack.slack_channel_left import SlackChannelLeft


class TestRemoveFromRoom(asynctest.TestCase):

    def setUp(self):
        self.slack_client = MagicMock()
        self.initialize_bm_plugin()

    def tearDown(self):
        self.initialize_bm_plugin()

    def initialize_bm_plugin(self):
        self.bm = BroadcastMessage(self.slack_client)
        self.bm.seed_initial_data = MagicMock()
        self.bm.add_to_room = CoroutineMock()
        self.bm.parse_wall_message = CoroutineMock()
        self.bm.room_membership = {}

    def test_invalid_input_single(self):
        msg = {}
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_not_in_any_rooms_single(self):
        msg = SlackChannelLeft(type="channel_left", channel="C024BE91L")
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_not_in_any_rooms_multiple(self):
        msg = SlackChannelLeft(channel="C1")
        yield from self.bm.process_message(msg)
        msg = SlackGroupLeft(channel="G1")
        yield from self.bm.process_message(msg)
        msg = SlackChannelLeft(channel="C2")
        yield from self.bm.process_message(msg)
        msg = SlackGroupLeft(channel="G2")
        yield from self.bm.process_message(msg)
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_remove_from_bogus_room(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = SlackChannelLeft(channel="C2")
        yield from self.bm.process_message(msg)
        expected = {
            "1": "fun1",
        }
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, expected)

    def test_remove_from_one_room(self):
        self.bm.room_membership = {"1": "fun1"}
        msg = SlackChannelLeft(channel="1")
        yield from self.bm.process_message(msg)
        self.assertEqual(self.bm.room_membership, {})

    def test_remove_from_multiple_rooms(self):
        self.bm.room_membership = {
            "1": "fun1",
            "2": "fun2",
            "3": "fun3",
            "4": "fun4",
            "5": "fun5",
        }
        msg = SlackChannelLeft(channel="2")
        yield from self.bm.process_message(msg)
        msg = SlackGroupLeft(channel="1")
        yield from self.bm.process_message(msg)
        msg = SlackGroupLeft(channel="4")
        yield from self.bm.process_message(msg)
        msg = SlackChannelLeft(channel="5")
        yield from self.bm.process_message(msg)
        expected = {
            "3": "fun3",
        }
        self.assertEqual(self.bm.room_membership, expected)
