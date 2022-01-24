from typing import List
from uuid import uuid4

from bbs3.domain.model.inbox import Inbox
from bbs3.domain.model.inbox_id import InboxId
from bbs3.domain.ports.outcoming.index_repository import IndexRepository
from bbs3.infrastructure.orm import Inbox as InboxModel
from bbs3.infrastructure.orm import Reply as RepliesModel
from bbs3.domain.model.signature import Signature


from bbs3.domain.model.reply import Replies, Reply


class IndexRepositoryAdapeter(IndexRepository):
    def __init__(self, session):
        self.session = session

    def get(self, inbox_id: InboxId):
        query = InboxModel.select().where(InboxModel.c.id == inbox_id)
        data = self.session.execute(query).first()
        return Inbox(**data._asdict())

    @classmethod
    def get_unique_id(cls) -> InboxId:
        return InboxId(uuid4().hex)

    def find_by_topic(self, topic: str) -> List[Inbox]:
        query = InboxModel.select().where(InboxModel.c.topic.like(f"%{topic}%"))
        data = self.session.cursor().execute(query).fetchall()
        return [Inbox(**item) for item in data]

    def save(self, inbox: Inbox):
        query = InboxModel.insert().values(
            id=str(inbox.id),
            topic=inbox.topic,
            owner=str(inbox.owner),
            expiration_date=str(inbox.expiration_date.timestamp()),
            allow_anonymous=int(inbox.allow_anonymous),
        )
        self.session.execute(query)
        self.session.commit()

    def change_topic(self, inbox: Inbox, new_topic: str):
        query = InboxModel.update().where(InboxModel.c.id == inbox.id).values(topic=new_topic)
        self.session.execute(query)
        self.session.commit()

    def get_all_inboxes(self):
        query = InboxModel.select()
        inboxes = self.session.execute(query)
        return [Inbox(**inbox) for inbox in inboxes]

    def get_replies(self, inbox: Inbox):
        query = RepliesModel.select().where(RepliesModel.c.inbox_id == inbox.id)
        data = self.session.execute(query).all()
        replies = Replies(inbox.id)
        for item in data:
            replies.add_reply(Reply(body=item["body"], signature=item["user"], timestamp=item["timestamp"]))
        return replies

    def get_replies_count(self, inbox: Inbox):
        query = RepliesModel.select().where(RepliesModel.c.inbox_id == inbox.id).count()
        data = self.session.execute(query).all()
        return data

    def save_reply(self, inbox: Inbox, user: Signature, reply: Reply):
        query = RepliesModel.insert().values(
            inbox_id=inbox.id, body=reply.body, user=str(user), timestamp=reply.timestamp
        )
        self.session.execute(query)
        self.session.commit()
