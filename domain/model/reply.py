from dataclasses import dataclass
from datetime import datetime
from collections.abc import Iterable
from bbs3.domain.model.inbox_id import InboxId
from bbs3.domain.model.signature import Signature
from bbs3.domain.model.ddd import Entity

from typing import List, Optional
from dataclasses import field


@dataclass
class Reply:
    body: str
    signature: Optional[Signature] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


class Replies(Entity, Iterable):
    def __init__(self, id: InboxId):
        self.id = id
        self.replies: List[Reply] = []

    def add_reply(self, reply: Reply):
        self.replies.append(reply)

    def __iter__(self):
        return iter(self.replies)

    def __contains__(self, value):
        return value in self.replies

    def __len__(self):
        return len(self.replies)
