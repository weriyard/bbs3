from dataclasses import dataclass
from datetime import datetime

from bbs3.domain.model.ddd import AggregateRoot, Entity
from bbs3.domain.model.excetpions import InboxChangeTopicError, InobxAddReplyError
from bbs3.domain.model.inbox_id import InboxId
from bbs3.domain.model.reply import Replies, Reply
from bbs3.domain.model.signature import Signature


@dataclass
class Inbox(Entity):
    id: InboxId
    topic: str
    owner: Signature
    expiration_date: datetime
    allow_anonymous: bool = False

    def user_can_get_replies(self, user: Signature) -> bool:
        return self.is_owner(user)

    def user_can_add_reply(self, user: Signature = None) -> bool:
        return isinstance(user, Signature) or self.allow_anonymous

    def owner_can_change_topic(self, user: Signature, replies: Replies) -> bool:
        return self.is_owner(user) and len(replies) == 0

    def is_owner(self, user: Signature):
        print(self.owner)
        print(user)
        return self.owner == user

    def __eq__(self, inbox):
        return isinstance(inbox, Inbox) and self.id == inbox.id


class InboxAggregate(AggregateRoot):
    def __init__(self, inbox: Inbox, replies: Replies, user: Signature) -> None:
        self.id = inbox.id
        self.inbox = inbox
        self.replies = replies
        self.user = user

    def add_reply(self, reply: Reply):
        if self.inbox.user_can_add_reply(self.user):
            self.replies.add_reply(reply)
        else:
            raise InobxAddReplyError("Can't add reply due to missing credentials.")

    def change_topic(self, new_topic):
        if self.inbox.owner_can_change_topic(self.user, self.replies):
            self.inbox.topic = new_topic
        else:
            raise InboxChangeTopicError
