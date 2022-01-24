from datetime import datetime
from typing import List

from bbs3.domain.model.inbox import Inbox, InboxAggregate
from bbs3.domain.model.inbox_id import InboxId
from bbs3.domain.model.reply import Replies, Reply
from bbs3.domain.model.signature import Signature
from bbs3.domain.model.excetpions import InboxWrongCredentials
from bbs3.domain.ports.outcoming.index_repository import IndexRepository


class InboxService:
    def __init__(
        self,
        inbox_repository: IndexRepository,
    ):
        self.inbox_repository = inbox_repository

    def create(self, topic, owner: Signature, expiration_date: datetime, allow_anonymous=False):
        inbox_id = self.inbox_repository.get_unique_id()
        inbox = Inbox(inbox_id, topic, owner, expiration_date, allow_anonymous)
        self.inbox_repository.save(inbox)
        return inbox.id

    def get_inbox(self, inbox_id: InboxId):
        return self.inbox_repository.get(inbox_id)

    def get_inbox_replies(self, signature: Signature, inbox_id: InboxId):
        inbox = self.get_inbox(inbox_id)
        if inbox.user_can_get_replies(signature):
            return self.inbox_repository.get_replies(inbox)
        else:
            raise InboxWrongCredentials

    def reply_to_inbox(self, user: Signature, inbox_id: InboxId, reply: str):
        inbox = self.get_inbox(inbox_id)
        replies = self.inbox_repository.get_replies(inbox)
        inbox_aggr = InboxAggregate(inbox, replies, user)
        inbox_reply = Reply(reply, user)
        inbox_aggr.add_reply(inbox_reply)
        self.inbox_repository.save_reply(inbox_aggr.inbox, inbox_aggr.user, inbox_reply)
        return reply

    def change_inbox_topic(self, inbox: Inbox, new_topic: str, user: Signature):
        replies = self.inbox_repository.get_replies(inbox)
        inbox_aggr = InboxAggregate(inbox, replies, user)
        inbox_aggr.change_topic(new_topic)
        self.inbox_repository.change_topic(inbox_aggr.inbox, new_topic)

    def find_by_topic(self, topic: str) -> List[Inbox]:
        return self.inbox_repository.find_by_topic(topic)
