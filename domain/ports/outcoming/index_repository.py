from bbs3.domain.model.inbox_id import InboxId
from bbs3.domain.model.inbox import Inbox
from bbs3.domain.model.reply import Replies, Reply
from bbs3.domain.model.signature import Signature

from abc import ABC, abstractmethod

from typing import List


class IndexRepository(ABC):
    @abstractmethod
    def get(self, inbox_id: InboxId) -> Inbox:
        pass

    @abstractmethod
    def save(self, inbox: Inbox) -> InboxId:
        pass

    @abstractmethod
    def find_by_topic(self, topic: str) -> List[Inbox]:
        pass

    @classmethod
    @abstractmethod
    def get_unique_id(cls) -> InboxId:
        pass

    @abstractmethod
    def change_topic(self, inbox: Inbox, new_topic: str):
        pass

    @abstractmethod
    def get_replies(self, inbox: Inbox) -> Replies:
        pass

    @abstractmethod
    def save_reply(self, inbox: Inbox, user: Signature, reply: Reply):
        pass
