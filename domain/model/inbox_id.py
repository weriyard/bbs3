from dataclasses import dataclass


@dataclass
class InboxId:
    id: str

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id
