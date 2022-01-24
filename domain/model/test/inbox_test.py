import unittest
import uuid
import datetime
from bbs3.domain.model.signature import Signature
from bbs3.domain.model.inbox import Inbox, InboxAggregate
from bbs3.domain.model.reply import Replies, Reply
from bbs3.domain.model.excetpions import InobxAddReplyError, InboxChangeTopicError


class InboxCreatinTestcCase(unittest.TestCase):
    def test_create_inbox(self):
        inbox_id = uuid.uuid4().hex
        topic = "Whatsss upp"
        owner = Signature("user##signature")
        expiration_date = datetime.datetime.now()
        allow_anonymous = False
        inbox = Inbox(inbox_id, topic, owner, expiration_date, allow_anonymous)
        self.assertIsInstance(inbox, Inbox)

    def test_comparation_different_inbox_id(self):
        inbox_1_id = uuid.uuid4().hex
        topic = "Whatsss upp"
        owner = Signature("user##signature")
        expiration_date = datetime.datetime.now()
        allow_anonymous = False
        inbox_1 = Inbox(inbox_1_id, topic, owner, expiration_date, allow_anonymous)
        inbox_2_id = uuid.uuid4().hex
        inbox_2 = Inbox(inbox_2_id, topic, owner, expiration_date, allow_anonymous)
        self.assertNotEqual(inbox_1, inbox_2)

    def test_comparation_same_inbox_id(self):
        inbox_1_id = uuid.uuid4().hex
        topic = "Whatsss upp"
        owner = Signature("user##signature")
        expiration_date = datetime.datetime.now()
        allow_anonymous = False
        inbox_1 = Inbox(inbox_1_id, topic, owner, expiration_date, allow_anonymous)
        inbox_2 = Inbox(inbox_1_id, topic, owner, expiration_date, allow_anonymous)
        self.assertEqual(inbox_1, inbox_1)
        self.assertEqual(inbox_1, inbox_2)


class InboxAddReplyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        inbox_id = uuid.uuid4().hex
        topic = "Whatsss upp"
        self.owner = Signature("owner_user##host")
        expiration_date = datetime.datetime.now()
        allow_anonymous = False
        self.inbox = Inbox(inbox_id, topic, self.owner, expiration_date, allow_anonymous)
        self.replies = Replies(self.inbox.id)
        self.replies.add_reply(Reply("message_1", Signature("test_user_1##host"), datetime.datetime.now()))
        self.replies.add_reply(Reply("message_2", Signature("test_user_2##host"), datetime.datetime.now()))

    def test_add_reply_by_user(self):
        user_signature = Signature("new_user##host")
        inbox_aggr = InboxAggregate(self.inbox, self.replies, user_signature)
        replies_count_before = len(inbox_aggr.replies)
        reply = Reply("message_3", user_signature, datetime.datetime.now())
        inbox_aggr.add_reply(reply)
        self.assertEqual(replies_count_before + 1, len(inbox_aggr.replies))

    def test_add_reply_as_anonymous_when_deny(self):
        user_signature = None
        inbox_aggr = InboxAggregate(self.inbox, self.replies, user_signature)
        reply = Reply("message_3", user_signature, datetime.datetime.now())
        with self.assertRaises(InobxAddReplyError):
            inbox_aggr.add_reply(reply)

    def test_add_reply_as_anonymous_when_allowed(self):
        user_signature = None
        self.inbox.allow_anonymous = True
        inbox_aggr = InboxAggregate(self.inbox, self.replies, user_signature)
        reply = Reply("message_3", user_signature, datetime.datetime.now())
        replies_count_before = len(inbox_aggr.replies)
        inbox_aggr.add_reply(reply)
        self.assertEqual(replies_count_before + 1, len(inbox_aggr.replies))

    def test_change_topic_by_owner_without_replies(self):
        new_topic = "Newww whastsupppp"
        replies = Replies(self.inbox.id)
        inbox_aggr = InboxAggregate(self.inbox, replies, self.owner)
        inbox_aggr.change_topic(new_topic)
        self.assertEqual(inbox_aggr.inbox.topic, new_topic)

    def test_change_topic_by_owner_when_replies(self):
        new_topic = "Newww whastsupppp"
        inbox_aggr = InboxAggregate(self.inbox, self.replies, self.owner)
        with self.assertRaises(InboxChangeTopicError):
            inbox_aggr.change_topic(new_topic)

    def test_change_topic_by_user(self):
        user = Signature("some_user##host")
        new_topic = "Newww whastsupppp"
        inbox_aggr = InboxAggregate(self.inbox, self.replies, user)
        with self.assertRaises(InboxChangeTopicError):
            inbox_aggr.change_topic(new_topic)
